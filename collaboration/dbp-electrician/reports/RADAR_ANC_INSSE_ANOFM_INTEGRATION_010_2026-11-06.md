# RADAR PREJOB — integrare ANC / INSSE / ANOFM — 06.11.2026 (Etapa 010)

**Stare:** staging SQLite local; fără import în DBP centrală sau schimbări în Drive master / RADAR public.

## Surse verificate și adăugate

### ANC / Ministerul Educației
- RNCP catalog: https://www.anc.edu.ro/rnc/rncp
- Standard ocupațional *Electrician în construcții civile și industriale*, ANC, versiunea 00, aprobat 21.06.2011, cod COR **istoric** 713708. Data revizuirii propuse 2015; nu a fost confirmată valabilitatea actuală a standardului: https://intern.anc.edu.ro/virtualanc/crud/standarde/standarde_ocupationale/brain/upload/Electrician.constructii.civile.industriale.pdf
- Catalogul Ministerului Educației conține SPP de nivel 3 pentru *Electrician constructor* și *Electrician exploatare joasă tensiune*. Acest lucru **nu dovedește** oferta efectivă a vreunei școli din București în 2026–2027: https://www.edu.ro/standarde-de-preg%C4%83tire-profesional%C4%83-pentru-calific%C4%83ri-profesionale-de-nivel-3-si-4-al-cadrului

### INSSE
- Serii definite și păstrate fără valori: TEMPO **FOM104D** (număr mediu de salariați), **FOM103D** (populație ocupată civilă după CAEN), disponibile în dicționarul existent din Drive. Portalul TEMPO a returnat 502 la interogarea directă. Fără valori inventate / extrapolate.

### ANOFM / AMOFM București
- Septembrie 2026: 5.281 șomeri înregistrați, 3.297 femei, rata de șomaj înregistrat 0,40%, publicat 29.10.2026.
  https://www.anofm.ro/bucuresti/04-rata-somajului-inregistrat-in-evidentele-amofm-bucuresti-in-luna-septembrie-2026/
- August 2026: 5.405 șomeri înregistrați, rata 0,41%, publicat 29.09.2026.
  https://www.anofm.ro/bucuresti/041-rata-somajului-inregistrat-in-evidentele-amofm-bucuresti-in-luna-august-2026/
- **Acestea sunt valori agregate pentru întreg municipiul**, nu observații despre Electrician. `occupation_uri` este NULL, verificat prin assert.

## QA bază SQLite nouă

- `PRAGMA integrity_check = ok`; `foreign_key_check=[]`
- 53 entități ESCO, 52 relații (21 esențiale, 31 opționale), 3 mapări COR/ISCED candidate, fără promovare semantică.
- 7 surse instituționale, 1 standard istoric, 2 calificări catalog, 5 definiții indicatori, 5 observații statistice agregate, 5 lacune explicite.
- Baza sursă Directiva 008: SHA256 `26b2da1aea8b5230ad5524fad86dd63f30902eeccc117b1ae6fe71f8a9201763`.
- Baza extinsă 010: SHA256 `98704b76cf272a6e8237eb3f954a121d42782c2ed69af655e650579a1fa6c11e`.
- Scriptul generator poate fi relansat pe aceeași bază sursă, fără duplicate.

## Lacune pentru validare
1. Verificarea standardului ANC actual pentru electrician.
2. Oferta școlară reală București, pe unitate SIIIR / an școlar, plus locuri aprobate.
3. Valorile reale INSSE TEMPO extrase pe perioadă, unitate, București separat de Ilfov.
4. Numărul posturilor vacante electrician, filtrat după COR și municipiu, dintr-un snapshot ANOFM.
5. Mapările ANC–ESCO–COR auditate de Qwen și aprobate de Adrian.

## Livrabile locale
`RADAR_PREJOB_Bucuresti_Electrician_ANC_INSSE_ANOFM_STAGING_010.sqlite`
`integrate_anc_insse_anofm_010.py`
`RADAR_PREJOB_010_manifest.json`

Acest lot reprezintă **integrare de proveniență + observații economice agregate**, nu finalizarea lanțului complet Electrician–educație–cerere de muncă.
