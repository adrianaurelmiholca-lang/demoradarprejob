# RADAR PREJOB — pilot Electrician, demonstrație locală (06.11.2026)

## Realizat
Am creat din staging SQLite al Directivei 008 un demonstrator HTML **offline, doar citire**, cu filtre de relație (essential/optional), tip concept (skill/knowledge), căutare și prezentarea lacunelor și a mapărilor candidate. Interfața nu este aplicația publică RADAR. Pachetul local include și scriptul reproductibil `build_demo.py`, raportul QA, registrul de audit QWEN, SQLite, CSV-uri și manifest cu SHA-256.

**QA local:** 1 ocupație, 52 skill/knowledge URI distincte, 21 relații esențiale + 31 opționale, 3 mapări candidate (COR 741101, 741110; ISCED-F 0713), 6 lacune. `PRAGMA integrity_check=ok`, `PRAGMA foreign_key_check=[]`. SHA-256 sursă salvată de utilizator: `d9668029b5da587e11bc6ea42690628cda30daa8ef1df68fe55ae9d2e95a6510`, identic cu cel al sursei din DB.

## Stare corectă
- Nicio mapare nu a fost declarată oficial echivalentă.
- Nu există date locale INSSE/ANOFM sau ofertă ANC/școlară numerică fabricate.
- ESCO source version neconfirmată independent; audit QWEN și aprobare Adrian încă necesare.
- Fără modificări master Drive, public RADAR, Cloudflare sau DBP centrală. Nu a fost identificată o conexiune verificată la DBP central.
- Pilotul este **demonstrabil tehnic local**, nu complet operațional în producție.

## Blocaje următoare
Identificarea bazei DBP centrale; snapshot oficial versionat ESCO; audit QWEN; surse ANC/ISMB, INSSE și ANOFM cu teritoriu și perioadă; eventual integrare într-un serviciu central cu backup și rollback.

Domeniul este RADAR PREJOB Faza 0 — București / Electrician. ESCO este doar o sursă de date, nu un produs separat.
