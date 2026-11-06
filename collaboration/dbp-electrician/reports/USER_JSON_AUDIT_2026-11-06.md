# RADAR PREJOB – verificare locală JSON ESCO Electrician

Data analizei: 2026-11-06

## Origine și integritate
- Fișier sursă: `occupation(1).customization`, încărcat în conversație de utilizator după deschiderea linkului API ESCO în Firefox.
- Dimensiune: 37278 octeți; JSON valid.
- SHA-256 al **octeților fișierului încărcat**: `d9668029b5da587e11bc6ea42690628cda30daa8ef1df68fe55ae9d2e95a6510`. Această amprentă nu este o semnătură oficială a Comisiei Europene.
- URI ocupație: `http://data.europa.eu/esco/occupation/4910419f-b4af-4f59-b544-9dbebc8a74f0`.
- Cod ESCO: `7411.1`; grupă ISCO: `7411`; etichetă RO: `electrician/electriciană`.
- Chei de relații: `_links.hasEssentialSkill` și `_links.hasOptionalSkill`.
- Versiune exactă: **nu este expusă explicit în acest JSON**; parametrul `selectedVersion=latest` este cunoscut din linkul furnizat utilizatorului, dar nu este demonstrat criptografic din fișier.

## Rezultatele comparației
- Esențiale în fișier: **21**.
- Opționale în fișier: **31**.
- Candidate: **21**.
- Corespondențe cu secțiunea esențială: **21 din 21**.
- Neconcordanțe de etichetă, tip sau relație: **0**.
- URI-uri esențiale suplimentare față de lista candidat: **0**.
- Relații esențiale/opționale suprapuse: **0**.

## Decizie
Datele sunt **confirmate prin comparație locală cu fișierul JSON furnizat de utilizator**, nu printr-o cerere HTTP executată și înregistrată de SOLON. Pentru PREJOB, atribuim `MATCHED_USER_SUPPLIED_JSON__PROVENANCE_PENDING`, nu `VERIFIED_OFFICIAL`.

Nu s-a efectuat inserare în DBP, deploy, actualizare `main` sau modificare de master.