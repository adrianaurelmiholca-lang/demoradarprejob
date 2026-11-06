# RADAR PREJOB – Etapa 012 – AMOFM București, istoric locuri vacante 2025

Data verificării: 2026-11-06. Continuare a etapei 011. **Staging**, nu DBP centrală.

## Import local executat
12 luni (ian.–dec. 2025), serie agregată pentru Municipiul București și **toate ocupațiile**, din raportul AMOFM București 2025, pagina 7, secțiunea II.c:
13.986, 14.683, 16.499, 14.955, 13.449, 15.962, 14.404, 14.605, 17.253, 15.280, 13.633, 14.673.

Sursă: https://www.anofm.ro/bucuresti/wp-content/uploads/sites/11/2018/11/RAPORT_ACTIVITATE_2025.pdf

Aceste 12 valori **nu** se adună ca total anual de posturi distincte. Ele nu măsoară ocupația Electrician, nu reprezintă un snapshot 2026 și nu permit inferarea unui deficit ocupațional. Indicatorul este stocat separat de ofertele individuale ANOFM (2026).

## Rezultat tehnic
- Fișier local: `RADAR_PREJOB_Bucuresti_Electrician_STAGING_012.sqlite`
- Import reproductibil: `integrate_radar_012.py`
- CSV cu proveniență și perioada: `RADAR_PREJOB_012_AMOFM_Bucuresti_Vacante_2025.csv`
- Pachet ZIP local: `RADAR_PREJOB_ETAPA_012_BUCURESTI_ELECTRICIAN.zip`.
- DB SHA256: `2d4cdd2f14897b03441de88ac3e348fcf5516557dcc7046ffa58634ca25bcb7d`.
- QA: SQLite `integrity_check=ok`, FK fără orfani, import idempotent cu SHA neschimbat.
- 53 entități ESCO, 52 relații ESCO, 3 mapări încă nevalidate, 4 intrări admitere, 2 oferte individuale ANOFM, 5 observații economice 2026, 12 observații agregate lunare 2025.

## Blocaje
Export INSSE TEMPO verificabil, extragere ANOFM completă pe cod COR și teritoriu, ofertă școlară completă SIIIR și legături ANC, audit QWEN, validare Adrian, DBP PostgreSQL central. Nu s-au modificat Drive master, Cloudflare, nici RADAR public.
