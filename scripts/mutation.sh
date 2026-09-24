#!/usr/bin/env bash
set -euo pipefail

# Forked macOS workers must not query SystemConfiguration through urllib/httpx.
export NO_PROXY='*' no_proxy='*'

# Refresh mutmut's test-to-mutant map so newly added tests are selected.
rm -rf -- mutants

mkdir -p reports
targets=reports/mutation-targets.bin
failed=reports/mutation-failed.bin
: > "$targets"
: > "$failed"

modules=()
add_module() {
  for known in "${modules[@]-}"; do
    [[ $known == "$1" ]] && return
  done
  modules+=("$1")
}
if [[ ${MUTATION_FULL:-0} == 1 ]]; then
  git ls-files -z 'src/volcano_sdk/*.py' > reports/mutation-source.bin
  while IFS= read -r -d '' path; do
    if [[ $path != src/volcano_sdk/_generated/* && $path != src/volcano_sdk/_tests/* && -f $path ]]; then
      add_module "$path"
    fi
  done < reports/mutation-source.bin
else
  for path in \
    src/volcano_sdk/locks.py \
    src/volcano_sdk/_lock_guard.py \
    src/volcano_sdk/_lock_renewer.py \
    src/volcano_sdk/_lock_worker.py; do
    add_module "$path"
  done

  base=${MUTATION_BASE_SHA:-origin/main}
  ancestor=$(git merge-base "$base" HEAD)
  changed() {
    git diff --name-only --diff-filter=ACMRT -z "$ancestor" HEAD
    git diff --name-only --diff-filter=ACMRT -z HEAD
    git ls-files -z --others --exclude-standard
  }
  changed > reports/mutation-changed.bin
  while IFS= read -r -d '' path; do
    if [[ $path == src/volcano_sdk/*.py && $path != src/volcano_sdk/_generated/* && $path != src/volcano_sdk/_tests/* && -f $path ]]; then
      add_module "$path"
    fi
  done < reports/mutation-changed.bin
fi

for path in "${modules[@]}"; do
  printf '%s\0' "$path" >> "$targets"
done

if [[ ${MUTATION_FULL:-0} == 1 ]]; then
  if ! mutmut run --max-children 1; then
    printf '%s\0' "full mutation run" >> "$failed"
  fi
else
  patterns=()
  for path in "${modules[@]}"; do
    module=${path#src/}
    module=${module%.py}
    patterns+=("${module//\//.}.x*")
  done
  if ! mutmut run --max-children 1 "${patterns[@]}"; then
    printf '%s\0' "scoped mutation run" >> "$failed"
  fi
fi

python -m scripts.mutation_results "$targets" "$failed"
