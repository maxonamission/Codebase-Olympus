#!/usr/bin/env bash
# Stop hook: draait de testsuite voordat Claude een sessie afrondt.
# Voorkomt dat Claude "klaar" zegt terwijl tests stuk zijn.
#
# Draait pytest met -x (stop bij eerste failure) en --tb=short.
# Exit-code 2 blokkeert de Stop-actie; Claude krijgt de failure-output
# en kan de tests alsnog fixen.

set -uo pipefail

# uv optioneel; als niet aanwezig, skip stil.
if ! command -v uv >/dev/null 2>&1; then
    exit 0
fi

# Alleen draaien als er een pytest-config aanwezig is.
if ! grep -q "\[tool.pytest" pyproject.toml 2>/dev/null; then
    exit 0
fi

output=$(uv run pytest -x --tb=short -q 2>&1)
status=$?

if [ $status -ne 0 ]; then
    echo "$output" >&2
    echo "" >&2
    echo "Stop-hook: pytest faalt — fix de tests voordat je de sessie afrondt." >&2
    exit 2
fi

exit 0
