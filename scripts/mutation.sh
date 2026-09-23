#!/usr/bin/env bash
# Select whole changed runtime modules; mutmut owns mutation and test execution.
set -euo pipefail

base="${MUTATION_BASE_SHA:-origin/main}"
if [[ "$base" != origin/main && ! "$base" =~ ^[0-9a-f]{40}$ ]]; then
  printf 'Invalid mutation base: %s\n' "$base" >&2
  exit 1
fi

scope="${MUTATION_SCOPE:-changed}"
if [[ "$scope" != changed && "$scope" != all ]]; then
  printf 'Invalid mutation scope: %s\n' "$scope" >&2
  exit 1
fi
mode="${MUTATION_DIFF_MODE:-merge-base}"
if [[ "$mode" != merge-base && "$mode" != direct ]]; then
  printf 'Invalid mutation diff mode: %s\n' "$mode" >&2
  exit 1
fi

selection_file="$(mktemp)"
trap 'rm -f "$selection_file"' EXIT
if [[ "$scope" == all ]]; then
  git ls-files -z -- src/volcano_sdk > "$selection_file"
elif [[ "$mode" == direct ]]; then
  git diff --name-only -z --diff-filter=ACMRT "$base..HEAD" -- src/volcano_sdk > "$selection_file"
else
  git diff --name-only -z --diff-filter=ACMRT "$base...HEAD" -- src/volcano_sdk > "$selection_file"
fi
git diff --name-only -z --diff-filter=ACMRT HEAD -- src/volcano_sdk >> "$selection_file"
git ls-files --others -z --exclude-standard -- src/volcano_sdk >> "$selection_file"

selected=(
  src/volcano_sdk/locks.py
  src/volcano_sdk/_lock_guard.py
  src/volcano_sdk/_lock_renewer.py
  src/volcano_sdk/_lock_worker.py
)
while IFS= read -r -d '' path; do
  [[ "$path" == src/volcano_sdk/*.py ]] || continue
  [[ "$path" != src/volcano_sdk/_generated/* ]] || continue
  found=false
  for existing in "${selected[@]}"; do
    if [[ "$existing" == "$path" ]]; then
      found=true
      break
    fi
  done
  if [[ "$found" == false ]]; then
    selected+=("$path")
  fi
done < "$selection_file"

patterns=()
for path in "${selected[@]}"; do
  [[ -f "$path" ]] || { printf 'Missing selected module: %s\n' "$path" >&2; exit 1; }
  module="${path#src/}"
  module="${module%.py}"
  module="${module//\//.}"
  module="${module%.__init__}"
  patterns+=("$module.*")
done

printf 'Mutation scope: %s\n' "$scope"
printf 'Selected module: %s\n' "${selected[@]}"
rm -f reports/mutation.json
if ! mutmut run "${patterns[@]}"; then
  mkdir -p reports
  printf '{"harness_error":"mutmut did not complete"}\n' > reports/mutation.json
  exit 1
fi
if ! python -m scripts.check_mutation "${selected[@]}"; then
  if [[ ! -f reports/mutation.json ]]; then
    mkdir -p reports
    printf '{"harness_error":"mutmut results are incomplete"}\n' > reports/mutation.json
  fi
  exit 1
fi
