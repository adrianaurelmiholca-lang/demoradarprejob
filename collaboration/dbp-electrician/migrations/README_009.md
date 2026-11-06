# RADAR PREJOB — migrare PostgreSQL staging 009

Artefactul local generat la 06.11.2026 transpune înregistrările deja existente în SQLite RADAR PREJOB (Directiva 008) într-un script SQL reproductibil pentru schema `radar_prejob_staging`.

## Limite și statut
- Schema PostgreSQL este **o propunere de staging**, nu o schemă canonică certificată și nici baza centrală în producție.
- SQL-ul nu a fost executat pe vreun server. Lipsesc endpointul, rolul de conectare verificat și un mediu PostgreSQL verificat.
- Scriptul generator verifică integritatea SQLite, FK-urile, 53 entități, 52 relații, 3 mapări candidate și cele șase lacune.
- 21 relații essential, 31 optional, 0 relații/mapări validate oficial.
- Nu se publică în RADAR și nu se modifică masterul Drive.
- Verificare Qwen + Adrian necesară pentru mapări COR/ISCED. Lipsesc date ANC/INSSE/ANOFM la nivel București.

## Livrare
Pentru rulare, se folosesc artefactele din pachetul `RADAR_PREJOB_POSTGRES_STAGING_009.zip` livrat în conversație: `build_postgres_staging_009.py`, `RADAR_PREJOB_POSTGRES_STAGING_009.sql`, `RADAR_PREJOB_MIGRATION_009_MANIFEST.json` și SQLite din Directiva 008.

Următorul gate: identificare server, backup, rol PostgreSQL limitat la staging și revizuirea schemei reale. Fără parole în repository.

**Observație:** prezența unui Google Sheet `DBP RADAR PREJOB – Pilot București v0.1.xlsx` nu demonstrează existența unei baze PostgreSQL în spate.
