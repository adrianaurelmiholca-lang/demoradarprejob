# Etapa 014 — Importator ESCO pentru ocupațiile Software developer și Graphic designer

Data: 09.11.2026 • **STAGING** • fără modificări DBP centrală / aplicație publică / master Drive.

Am creat local un importator Python și patru teste automate:
- acceptă doar răspunsuri JSON a căror proprietate `uri` corespunde exact ocupației înregistrate;
- citește `_links.hasEssentialSkill` și `_links.hasOptionalSkill`;
- respinge URI-uri invalide și semnalează duplicate;
- scrie CSV cu relații în statut `PENDING_HUMAN_REVIEW` și manifest SHA-256;
- fără date, nu fabrică relații; versiunea API rămâne `UNKNOWN_UNLESS_SEPARATELY_DOCUMENTED`.

**Teste:** 4/4 passed, pe fixture sintetice. Testele confirmă logica importatorului, NU răspunsurile API oficiale.

URI-uri din DBP MASTER:
- Software developer: `PREJOB-ESCO-OCC-0001` — `http://data.europa.eu/esco/occupation/f2b15a0e-e65a-438a-affb-29b9d50b77d1` (108 relații istorice candidate, URI skill lipsă).
- Graphic designer: `PREJOB-ESCO-OCC-0002` — `http://data.europa.eu/esco/occupation/69bcbb0a-8d80-4ecd-b0a4-9adea2a40de2` (0 relații în master).

**Limitare actuală:** mediul de execuție nu a putut accesa direct `https://ec.europa.eu/esco/api/resource/occupation` (DNS indisponibil). Nu s-au importat noi date ESCO oficiale. Scriptul lucrează doar pe răspuns JSON oficial furnizat separat.

Documentație oficială: https://esco.ec.europa.eu/en/use-esco/use-esco-services-api/esco-web-service-api

**Următor pas:** obținere și păstrare JSON brut pentru ambele ocupații; import, audit și abia apoi integrare centrală cu validare umană.