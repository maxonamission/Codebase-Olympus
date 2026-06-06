---
type: story
project: GC
epic: E26
story_id: OL_E26_S1
legacy_id: E1-01
track: app
status: doing
prioriteit: middel
---

# Story OL_E26_S1: Graph visualisatie verbeteren + interactieve node-exploratie

## Doel
De knowledge graph visualisatie transformeren van een passief beeld naar een interactief navigatie-instrument. Betere layout, klik-interactie, en de mogelijkheid om vanuit de graph een leersessie te starten.

## Scope

### 1. Betere layout
- Vervang de simpele force-directed layout door een meer geschikte aanpak voor een DAG met 800+ nodes
- Groepeer nodes per type (G/V/C/I) in visueel herkenbare clusters
- Voorkom dat nodes aan de randen kleven
- Zoom en pan ondersteuning

### 2. Exploratie (laag risico)
- Klik op een node → info-panel met: titel, beschrijving, mastery-status, prerequisites, post-requisites
- Highlight de directe buren (prerequisites + post-requisites) bij hover/selectie
- Toon of de node "ready" is (prerequisites voldaan)

### 3. Vrije start (hoger risico)
- In het info-panel: "Oefen deze knoop" knop
- Start een mini-sessie op die specifieke node + directe prerequisites die nog niet beheerst zijn
- BKT-model vangt fouten op — als de leerling faalt, stuurt het systeem terug

## Acceptatiecriteria
- [ ] Graph toont 800 nodes zonder overlap of rand-clustering
- [ ] Klik op node toont info-panel
- [ ] "Oefen deze knoop" start een sessie gefocust op die node
- [ ] Zoom/pan werkt op desktop en tablet

## Geschat
Frontend: GraphView.jsx rewrite + NodeInfoPanel component + mini-sessie API
