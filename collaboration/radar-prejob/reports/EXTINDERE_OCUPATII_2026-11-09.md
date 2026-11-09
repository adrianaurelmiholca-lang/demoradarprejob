# Extindere RADAR PREJOB: ocupațiile 2 și 3 — 09.11.2026

## Inventar demonstrat din Drive
Sursă: [DBP ESCO — MASTER DATABASE](https://docs.google.com/spreadsheets/d/1QFQi9TYH4jaloa490PGebCc-1C8dx451j0aEdTiBLPw/edit).

| ID PREJOB | Ocupație | ISCO-08 | Relații candidate în registru | URI skill completat |
|---|---|---:|---:|---:|
| PREJOB-ESCO-OCC-0001 | Software developer | 2512 | 108: 9 cunoștințe esențiale, 15 abilități esențiale, 70 cunoștințe opționale, 14 abilități opționale | 0 |
| PREJOB-ESCO-OCC-0002 | Graphic designer | 2166 | 0 | 0 |

Cele 108 relații provin dintr-un inventar istoric derivat din sursă secundară și nu sunt încă verificate la API-ul oficial. **Nu sunt 108 competențe oficial validate.** Absența relațiilor Designer grafic nu înseamnă că ocupația nu are competențe, ci doar că registrul este încă nepopulat.

## Mapări candidate deja existente
- Software developer: COR 251202, 251205; ISCED-F 0613; mapări semantice în așteptare.
- Graphic designer: COR 216611, 216601; ISCED-F 0211; mapări semantice în așteptare.

## Gate-uri de import
1. GET ESCO API pentru fiecare URI ocupațional, HTTP 200 cu `uri` potrivit și relații `_links.hasEssentialSkill` / `_links.hasOptionalSkill`.
2. Salvarea fișierului brut, SHA-256, versiunii disponibile și datei răspunsului.
3. Construirea registrului canonic de competențe pe URI, nu după etichete derivate din mirror.
4. Compararea cu inventarul istoric software; adăugarea structurii Designer grafic.
5. Legarea la RADAR PREJOB București, cu date economice și educaționale distincte, fără a extrapola din indicatori municipali generali.
6. Audit Qwen și aprobare Adrian înainte de validarea semantică/publicare.

## Stare
Registrul de extindere a fost creat în ramura de staging. Drive master, producția și DBP centrală nu au fost modificate. API direct și importul pentru aceste două ocupații nu sunt încă confirmate.
