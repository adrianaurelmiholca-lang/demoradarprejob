# Etapa 011 – RADAR PREJOB București Electrician (06.11.2026)

Staging local SQLite + import idempotent, fără modificare DBP central, master Drive, Cloudflare sau RADAR public.

- 4 rânduri oficiale admitere 2026 din 2 unități: Colegiul Tehnic Mihai Bravu (487: 14 locuri / 6 repartizați, 716 dual: 28 / 14); Colegiul Tehnic Energetic (508: 28 / 21, 509: 28 / 9). **Totalul strict al celor patru rânduri: 98 locuri / 50 repartizați**. Nu este oferta completă București; nu se echivalează automat cu COR sau ANC.
- 2 pagini ANOFM individuale: oferta 3290121 COR 741101, 5 locuri nou create, București Sector 3, afișată valabilă până 06.12.2026; oferta 3420855 COR 741307, 1 loc vacant, Sector 4, valabilă până 18.11.2026. **Nu sunt totalul pieței și nu confirmă disponibilitate live**. 741307 nu este mapat automat cu ESCO 7411.1.
- INSSE FOM104D: registru sursă păstrat, **fără valori importate** întrucât nu este disponibil extras direct verificabil.
- Tabele noi: `official_education_admission` = 4, `official_anofm_job_snapshot` = 2, `radar_011_source_log` = 7. Păstrate 53 entități ESCO, 52 relații, 5 observații statistice din Etapa 010.
- QA: integritate OK, FK fără orfani, reimport idempotent cu SHA-256 neschimbat, mapări ESCO/COR/ANC neaprobate.
- Scriptul complet și SQLite livrate în pachetul local `RADAR_PREJOB_ETAPA_011_BUCURESTI_ELECTRICIAN.zip`.

Surse:
- https://admitere.edu.ro/Pages/SpecPerLic.aspx?Jud=4&Lic=11554070
- https://admitere.edu.ro/Pages/SpecPerLic.aspx?Jud=4&Lic=11548670
- https://mediere.anofm.ro/app/module/mediere/job/3290121
- https://mediere.anofm.ro/app/module/mediere/job/3420855
- https://statistici.insse.ro/tempoins/index.jsp?ind=FOM104D&lang=ro&page=tempo3

Lacune: export INSSE, snapshot ANOFM complet, evidența școlară completă/SIIIR, ANC actual, QWEN+Adrian, acces verificat la DBP centrală.
