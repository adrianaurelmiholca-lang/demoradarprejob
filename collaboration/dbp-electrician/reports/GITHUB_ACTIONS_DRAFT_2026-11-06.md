# PREJOB — Pregătire GitHub Actions ESCO (06.11.2026)

## Stare: PREGĂTIT, NEACTIVAT
Workflow: `.github/workflows/esco-electrician-validation.yml`, salvat doar în ramura `work/dbp-bucuresti-multiai-2026-11-04`.

Control static al configurației: **6/6 verificări trecute**:
1. exclusiv `workflow_dispatch` (fără push, pull_request sau schedule);
2. `permissions: contents: read`;
3. jobul are gard explicit pentru ramura `work/dbp-bucuresti-multiai-2026-11-04`;
4. fără deploy / Cloudflare / comenzi de publicare;
5. rezultatele sunt transmise doar ca artefact GitHub Actions, retenție 7 zile;
6. marcaj DRAFT ONLY pentru aprobarea umană.

## Ce ar face după o aprobare separată
- checkout doar pentru citire;
- 12 teste offline din pachetul de validator (neexecutate de GitHub Actions în prezent);
- GET HTTPS la endpointul oficial ESCO cu `latest` sau `v1.2.0`;
- scriere locală în runner a manifestului, comparației CSV și (numai la HTTP 200 valid) JSON raw cu SHA-256;
- uploadul artefactelor pentru controlul uman, fără commit/INSERT SQL.

## Limitare de activare
Conform documentației GitHub, pentru butonul standard `Run workflow`, workflow-ul trebuie să fie prezent în ramura implicită. **Nu există aprobare pentru această modificare în `main`**, prin urmare nu s-a activat și nu s-a încercat nicio rulare.

## Atenționări
- Un runner GitHub poate avea acces la API ESCO, dar succesul nu este garantat.
- Artefactele sunt date publice ESCO în repository public; nu se introduc documente private, tokenuri sau date personale.
- Nu este definit niciun serviciu cu plată, dar executarea depinde de limitele/condițiile GitHub.
- Chiar dacă apelul reușește, promovarea `VERIFIED_OFFICIAL` necesită încă verificarea versiunii și validarea umană.
- Pentru activare și orice schimbare în `main` este necesară aprobare expresă.

Documentație: https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
