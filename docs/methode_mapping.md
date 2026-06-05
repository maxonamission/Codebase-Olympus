# Methode-mapping — onderhoud en proces

De methode-mapping verbindt een **schoolmethode + hoofdstuk** aan de
knoop-IDs uit de knowledge graph die in dat hoofdstuk behandeld zijn. Ze
voedt twee mechanismen:

1. **Intake** (`apply_methode_profile`) — zet BKT-priors: knopen tot en
   met het opgegeven hoofdstuk krijgen prior 0.70 ("behandeld, te
   verifiëren"), de rest 0.10.
2. **Bijspijker-modus** (M1-03, `BijspijkerPlanner`) — bepaalt de
   *doelset*: alle knopen tot en met het hoofdstuk van de klas plus hun
   prerequisites.

## Bestandslocatie en structuur

Alles staat in één bestand: **`data/methode_mapping.json`**. (De
M1-03-story noemde een per-methode-directory; we houden bewust het
bestaande, al-bedrade enkele bestand aan om de werkende intake-route niet
te breken.)

```json
{
  "methoden": {
    "fortuna": {
      "naam": "Fortuna",
      "language": "lat",
      "hoofdstukken": {
        "1": {
          "description": "Korte omschrijving van het hoofdstuk",
          "node_ids": ["LAT-G-MORF-NAAMVAL-INTRO", "..."]
        }
      }
    }
  }
}
```

- `language`: `lat` of `grc`.
- Hoofdstuksleutels zijn strings van opeenvolgende getallen vanaf `"1"`.
- `node_ids`: platte lijst; grammatica (`-G-`) en vocabulaire (`-V-`)
  worden afgeleid uit het ID-patroon — geen aparte sublijsten nodig.
- Sleutels die met `_` beginnen (bijv. `_comment`) worden genegeerd.

## Een nieuwe methode of editie toevoegen

1. Voeg onder `methoden` een nieuwe sleutel toe (bijv. `"roma_2025"`),
   met `naam`, `language` en `hoofdstukken`.
2. Vul per hoofdstuk een `description` en de `node_ids` die in dat
   hoofdstuk worden behandeld. Gebruik bestaande graph-IDs.
3. Houd hoofdstukken **opeenvolgend** (1, 2, 3, …) en zet elke knoop in
   **hooguit één** hoofdstuk per methode.
4. Valideer tegen de graph:
   ```bash
   uv run python -c "from pathlib import Path; \
     from gymnasium_classica.graph.loader import load_graph; \
     from gymnasium_classica.diagnostic.methode_profile import \
       load_methode_mapping, validate_methode_mapping; \
     print(validate_methode_mapping(load_methode_mapping(), load_graph(Path('data/graph'))) or 'OK')"
   ```
   `validate_methode_mapping` controleert: alle knopen bestaan, geen
   duplicaten binnen een methode, hoofdstukken opeenvolgend vanaf 1.
5. `tests/test_methode_mapping_validator.py` borgt dit ook in CI.

## Demo-walkthrough (bijspijker)

Een leerling op **Pallas hoofdstuk 4** kiest in de onboarding
bijspijker-modus, methode `pallas`, hoofdstuk `4`. De
`BijspijkerPlanner` neemt de doelset = knopen van hoofdstuk 1 t/m 4 +
prerequisites, diagnosticeert wat nog niet beheerst is, en plant een
versneld inhaalpad dat elke sessie afsluit met een vertaling uit
hoofdstuk 4. Zie `docs/PILOT_GUIDE.md` (bijspijker-scenario) en
**Keuze 18** in `ONTWERPKEUZES_GYMNASIUM_CLASSICA.md`.

## Status van de huidige mapping

De mapping is een **PoC**: Fortuna (LAT, hfdst. 1-5), SPQR (LAT, hfdst.
1) en Pallas (GRC, hfdst. 1-6) op basis van de leerjaar-1-knopen. De
definitieve hoofdstukindeling per editie wordt door de externe
klassieke-taleninstituut-partner gevalideerd.
