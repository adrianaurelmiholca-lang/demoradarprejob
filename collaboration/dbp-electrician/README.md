# Directiva SOLON 006 — Validator ESCO Electrician

**Destinație:** exclusiv ramura `work/dbp-bucuresti-multiai-2026-11-04`.

- `data/electrician_candidate_skills.csv`: 21 relații CANDIDATE raportate anterior de Qwen; **nu sunt date validate oficial**.
- `scripts/validate_esco_electrician.py`: doar GET ESCO; citește date, salvează răspunsul brut doar dacă HTTP 200 și JSON valid; calculează SHA-256; extrage relațiile din `_links.hasEssentialSkill` și `_links.hasOptionalSkill`, compară URI-urile și produce CSV/manifest.
- `tests/test_validate_esco_electrician.py`: teste fără internet.
- `tests/fixture_esco_synthetic.json`: exemplu **SINTETIC** pentru teste; nu se folosește în DBP.

## Comenzi

```sh
python -m unittest discover -s tests -v
python scripts/validate_esco_electrician.py --candidates data/electrician_candidate_skills.csv --out reports/live
```

Test parser offline (nu este verificare ESCO oficială):

```sh
python scripts/validate_esco_electrician.py --candidates data/electrician_candidate_skills.csv --fixture tests/fixture_esco_synthetic.json --out reports/fixture
```

## Reguli

1. Dacă DNS, HTTP sau JSON eșuează, toate înregistrările primesc `NOT_TESTED` și procesul are cod de ieșire 2.
2. HTTP 200 nu produce automat `VERIFIED_OFFICIAL`: o potrivire directă fără diferențe devine `API_RELATION_CONFIRMED_VERSION_UNVERIFIED`; neconcordanțele de etichetă, tip sau relație devin `API_RELATION_REQUIRES_REVIEW`. Promovarea în stratul validat DBP necesită verificarea versiunii și a provenienței.
3. `NOT_FOUND_IN_API` nu înseamnă că URI-ul nu există: înseamnă că nu a fost găsit în relațiile ocupației din răspunsul obținut.
4. Datele nu sunt încă importate în DBP, nu există API cu plată și nu se modifică `main`, Cloudflare, Google Drive sau datele de producție.
5. **Nu comiteți automat în GitHub** răspunsurile API sau artefactele de test fără verificarea provenienței și a permisiunilor.