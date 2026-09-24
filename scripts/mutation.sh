#!/usr/bin/env bash
set -euo pipefail

# Forked macOS workers must not query SystemConfiguration through urllib/httpx.
export NO_PROXY='*' no_proxy='*'

shard_count=8
paths=()
while IFS= read -r -d '' path; do
  if [[ $path == src/volcano_sdk/*.py && $path != src/volcano_sdk/_generated/* && -f $path ]]; then
    paths+=("$path")
  fi
done < <(git ls-files --cached --others --exclude-standard -z -- src/volcano_sdk)

if (( ${#paths[@]} == 0 )); then
  echo 'No handwritten SDK runtime modules found' >&2
  exit 1
fi

if [[ ${1:-} == --matrix && $# == 1 ]]; then
  printf '['
  for ((shard = 0; shard < shard_count; shard++)); do
    ((shard == 0)) || printf ','
    printf '%s' "$shard"
  done
  printf ']\n'
  exit
fi
if (( $# != 0 )); then
  echo 'Usage: scripts/mutation.sh [--matrix]' >&2
  exit 2
fi

if [[ -n ${MUTATION_SHARD:-} ]]; then
  if [[ ! $MUTATION_SHARD =~ ^(0|[1-9][0-9]*)$ ]] || (( MUTATION_SHARD >= shard_count )); then
    echo "Invalid mutation shard: $MUTATION_SHARD" >&2
    exit 2
  fi
fi

mkdir -p reports
targets=reports/mutation-targets.bin
failed=reports/mutation-failed.bin
: > "$targets"
: > "$failed"
patterns=()
for index in "${!paths[@]}"; do
  if [[ -n ${MUTATION_SHARD:-} ]] && (( index % shard_count != MUTATION_SHARD )); then
    continue
  fi
  path=${paths[$index]}
  printf '%s\0' "$path" >> "$targets"
  module=${path#src/}
  module=${module%.py}
  if [[ $module == */__init__ ]]; then
    module=${module%/__init__}
  fi
  patterns+=("${module//\//.}.x*")
done

if (( ${#patterns[@]} == 0 )); then
  echo 'Selected mutation shard has no runtime modules' >&2
  exit 1
fi

# A fresh run must not inherit stale test-to-mutant mappings or verdicts.
rm -rf -- mutants
if ! mutmut run --max-children 1 "${patterns[@]}"; then
  printf '%s\0' 'mutation run' >> "$failed"
fi

python -m scripts.mutation_results "$targets" "$failed"
