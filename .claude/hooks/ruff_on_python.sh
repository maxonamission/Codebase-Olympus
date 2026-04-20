#!/usr/bin/env bash
# PostToolUse hook: draait ruff op Python-bestanden die Claude zojuist
# heeft bewerkt. Zo ziet Claude lint-issues meteen in dezelfde turn.
#
# Input: JSON via stdin met daarin tool_input.file_path.
# Output: ruff-output op stdout/stderr (zichtbaar voor Claude).
# Exit-code: altijd 0 (non-blocking); ruff-failures worden als tekst
# doorgegeven zodat Claude ze oppakt zonder de hook te laten crashen.

set -uo pipefail

# JSON-payload van Claude Code inlezen.
payload=$(cat)

# file_path uit tool_input extraheren via python (jq niet gegarandeerd aanwezig).
file_path=$(python3 -c "
import json, sys
try:
    data = json.loads(sys.argv[1])
    print(data.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" "$payload")

# Alleen Python-bestanden; skip anders stil.
case "$file_path" in
    *.py)
        ;;
    *)
        exit 0
        ;;
esac

# Bestand moet bestaan (Edit op een verwijderd bestand komt niet voor, maar safe is safe).
[ -f "$file_path" ] || exit 0

# Ruff check + format; uv is in PATH (anders skip).
if command -v uv >/dev/null 2>&1; then
    uv run ruff check --fix "$file_path" 2>&1 || true
    uv run ruff format "$file_path" 2>&1 || true
fi

exit 0
