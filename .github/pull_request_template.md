<!--
PR-template voor Codebase-Olympus. Vul elk blok in.
Zie CLAUDE.md § "Review-skills" voor wanneer welke skill draaien.
-->

## Samenvatting

<!-- Wat verandert deze PR, en waarom? Maximaal 3 bullets. -->

-
-
-

## Testplan

<!-- Hoe is deze wijziging geverifieerd? -->

- [ ] `uv run ruff check .` en `uv run ruff format --check .` groen
- [ ] `uv run mypy src/` groen
- [ ] `uv run pytest -q` groen
- [ ] `uv run python scripts/check_story_status.py --mode=full` groen
- [ ] Aanvullend handmatig getest (indien relevant):

## Geraakte stories

<!--
Welke stories raakt deze PR? Volg OS-06-conventie: verplaats tussen
backlog/doing/done en werk EPICS.md bij. Lijst ze hieronder.
-->

- [ ] `stories/done/OS-XX.md` (was `doing` / `backlog`) — AC afgevinkt, status in EPICS.md bijgewerkt

## Review

<!-- Laag 5 van de ontwikkelstraat. Zie CLAUDE.md voor de triggers. -->

- [ ] `/review` gedraaid; commentaar verwerkt of expliciet besproken
- [ ] `/security-review` gedraaid — **verplicht** bij wijzigingen in:
  - `src/gymnasium_classica/api/auth*` of token-afhandeling
  - `src/gymnasium_classica/api/database.py` of sqlite-queries
  - endpoints die user-input accepteren (intake, session, user)
  - externe API-aanroepen (toekomstig: TTS, OCR, LLM)
  - dependency-upgrades in `pyproject.toml`

## Notities voor de reviewer

<!-- Optioneel. Context die niet uit de diff blijkt: afwegingen,
     alternatieven die je hebt overwogen, bekende beperkingen. -->
