# RADAR PREJOB — Directiva 006, revizie de siguranță (04.11.2026)

## Rezultate
- 21 URI-uri candidate distincte, încă NEVALIDATE ca relații ESCO oficiale.
- Validatorul detectează schimbarea relației `essential`/`optional`, nepotrivirea `skill`/`knowledge` și etichetele neconcordante.
- Un HTTP 200 nu promovează automat statutul `VERIFIED_OFFICIAL`: fără confirmare explicită a versiunii, rezultatul maxim este `API_RELATION_CONFIRMED_VERSION_UNVERIFIED`.
- Teste offline: **9/9 PASS**.
- GET live ESCO: **eșec DNS** (`Temporary failure in name resolution`) — **21 NOT_TESTED, 0 validate independent**.
- Un test fixture sintetic cu două relații a trecut, dar nu reprezintă dovadă oficială.

## Decizie
Nu importăm încă relațiile în stratul validat DBP. Nu presupunem mapări ESCO–COR. Următoarea operație este execuția într-un mediu cu acces HTTPS la API și păstrarea unui răspuns original cu SHA-256 și versiune verificată.

## Limite respectate
Ramura `main`, producția RADAR, Cloudflare și masterele Google Drive nu au fost modificate. Fără utilizare de API cu plată.
