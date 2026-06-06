---
type: story
project: GC
epic: E17
story_id: OL_E17_S2
legacy_id: D1-02
track: app
status: done
prioriteit: middel
---

# Story OL_E17_S2: Auth endpoints: register + login

## Doel
POST /auth/register (email + wachtwoord → user_id + token), POST /auth/login (email + wachtwoord → token). Simpele token-auth (UUID-based of JWT). Password hashing met bcrypt/passlib.

## Input
models/user.py, api/database.py

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
api/routes/auth.py, password hashing, token generatie, auth middleware

## Geschat
—
