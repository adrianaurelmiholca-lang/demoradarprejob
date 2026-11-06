# Directiva 008 — Reconciliere RADAR PREJOB, pilot București — 06.11.2026

## Identificare surse existente, fără modificări

1. **DBP RADAR PREJOB – Pilot București v0.1.xlsx** (Google Drive ID `1ebb9LxjZ-RSioIP-rbTy5YlHBAwAGgEl`): 24 secțiuni; sursele, organizațiile și teritoriile sunt parțial populate; tabelele de entități ESCO, relații ESCO, calificări, ocupații COR, indicatori/observații și mapări semantice sunt încă goale.
2. **RADAR PREJOB – Dicționarul bazei de date Faza 0** (ID `1n3PIEMlHgskrJBqo554H1KUtcdsiqSIESA7KGLIVHx0`): definiții, vocabular, controale QA, tabelare viitoare PostgreSQL. Regulile interzic transformarea ipotezelor în date validate.
3. **DBP ESCO — MASTER DATABASE** (ID `1QFQi9TYH4jaloa490PGebCc-1C8dx451j0aEdTiBLPw`): 3 ocupații și 108 rânduri în registrul de skills. Ocupația Electrician are deja `PREJOB-ESCO-OCC-0003`; mapările `COR-MAP-0005`, `COR-MAP-0006` și `EDU-MAP-0003` există deja ca relații semantice candidate.

## Integrarea realizată în staging local

A fost generat un SQLite *pentru RADAR PREJOB*, nu o bază ESCO independentă, folosind intrarea `PREJOB_Electrician_52_relatii_din_JSON.csv` (SHA-256 `742e5cc95d891e1d8092080b3dd961119a6a12297411ad1c0b9ef3fc4ae9fb17`).

Conține:
- 1 sursă de referință `src_esco_api`;
- 1 teritoriu pilot `ter_b` (București) — **fără a infera cerere de muncă locală**;
- 53 entități ESCO (1 ocupație + 52 skill/knowledge URI);
- 52 relații (21 essential + 31 optional);
- 3 mapări candidate (2 COR, 1 ISCED-F 0713);
- 6 lacune urmărite (ANC, trasee educaționale, INSSE, ANOFM, conexiune DBP și versiunea ESCO);
- 1 jurnal de import.

**Teste executate:** `PRAGMA integrity_check = ok`, `foreign_key_check = []`, import repetat fără dubluri (idempotent), numărări 52/21/31, 0 relații oficial validate.

**Proveniență:** JSON salvat de utilizator în browser; SHA-256 sursă `d9668029b5da587e11bc6ea42690628cda30daa8ef1df68fe55ae9d2e95a6510`. Versiunea ESCO nu a fost independent confirmată. Urmează audit QWEN și aprobarea Adrian.

## Ce NU s-a făcut

Nu s-au schimbat fișierele master Google Drive, RADAR public, Cloudflare, sau baza de producție. Nu există acces dovedit la serverul PostgreSQL DBP central; nu se presupune că pilotul XLSX este un DB server. Integrarea la DBP central așteaptă conexiune și structură verificată. Nu se promovează `VALIDATA_SURSA` doar din fișierul local.

## Mapare la coloanele pilotului RADAR

- `10_ENTITATE_ESCO` ↔ `esco_entity` (URI, tip, etichetă, ISCO, sursă, status);
- `11_RELATIE_ESCO` ↔ `esco_relation` (entitate sursă, relație, țintă, sursă);
- `12_MAPARE_SEMANTICA` ↔ `semantic_mapping` (COR/ISCED candidate, status);
- `01_SURSA` ↔ `source_reference` (proveniență și checksum);
- `03_TERITORIU` ↔ `territory` (identificator existent);
- `23_IMPORT_LOG` ↔ `import_audit`.

Tabele de indicatori/observații economice rămân nepopulate; datele ANOFM/INSSE nu se deduc din ESCO.

## Următorii pași

1. Verificare printr-un snapshot ESCO oficial versionat și trecerea la `VALIDATA_SURSA` unde este justificat.
2. Audit QWEN și validare Adrian pentru COR/ISCED.
3. Legarea calificărilor ANC și a traseelor educaționale reale din București.
4. Obținerea unui endpoint DBP securizat și import idempotent în schema canonică; fără chei în repository.
