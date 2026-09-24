#!/usr/bin/env bash
set -euo pipefail

# Forked macOS workers must not query SystemConfiguration through urllib/httpx.
export NO_PROXY='*' no_proxy='*'

paths=()
modules=()
while IFS= read -r -d '' path; do
  if [[ $path == src/volcano_sdk/*.py && $path != src/volcano_sdk/_generated/* && $path != src/volcano_sdk/_tests/* && -f $path ]]; then
    module=${path#src/}
    module=${module%.py}
    if [[ $module == */__init__ ]]; then
      module=${module%/__init__}
    fi
    module=${module//\//.}
    if [[ ! $module =~ ^[a-zA-Z_][a-zA-Z_0-9]*(\.[a-zA-Z_][a-zA-Z_0-9]*)*$ ]]; then
      echo "Invalid Python runtime module: $path" >&2
      exit 1
    fi
    for existing in "${modules[@]-}"; do
      if [[ $module == "$existing" ]]; then
        echo "Duplicate Python runtime module: $module" >&2
        exit 1
      fi
    done
    paths+=("$path")
    modules+=("$module")
  fi
done < <(git ls-files --cached --others --exclude-standard -z -- src/volcano_sdk)

if (( ${#paths[@]} == 0 )); then
  echo 'No handwritten SDK runtime modules found' >&2
  exit 1
fi
if [[ ${1:-} == --matrix && $# == 1 ]]; then
  printf '['
  for index in "${!modules[@]}"; do
    ((index == 0)) || printf ','
    printf '"%s"' "${modules[$index]}"
  done
  printf ']\n'
  exit
fi
if (( $# != 0 )); then
  echo 'Usage: scripts/mutation.sh [--matrix]' >&2
  exit 2
fi

mkdir -p reports
targets=reports/mutation-targets.bin
failed=reports/mutation-failed.bin
: > "$targets"
: > "$failed"
patterns=()
for index in "${!paths[@]}"; do
  if [[ -n ${MUTATION_MODULE:-} ]] && [[ ${modules[$index]} != "$MUTATION_MODULE" ]]; then
    continue
  fi
  path=${paths[$index]}
  selected_path=$path
  printf '%s\0' "$path" >> "$targets"
  patterns+=("${modules[$index]}.x*")
done

if (( ${#patterns[@]} == 0 )); then
  echo "Unknown mutation module: ${MUTATION_MODULE:-}" >&2
  exit 2
fi

# A fresh run must not inherit stale test-to-mutant mappings or verdicts.
rm -rf -- mutants

# Mutmut rejects an exact wildcard for a module with no functions. Record that
# module explicitly instead of treating a native no-match assertion as a kill.
if [[ -n ${MUTATION_MODULE:-} ]] && ! python -c '
import sys
from pathlib import Path
from scripts.mutation_results import has_functions
raise SystemExit(0 if has_functions(Path(sys.argv[1])) else 1)
' "$selected_path"; then
  python -m scripts.mutation_results "$targets" "$failed"
  exit
fi

if ! mutmut run --max-children 1 "${patterns[@]}"; then
  printf '%s\0' 'mutation run' >> "$failed"
fi

python -m scripts.mutation_results "$targets" "$failed"
