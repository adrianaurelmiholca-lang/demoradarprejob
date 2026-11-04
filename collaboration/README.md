# RADAR PREJOB — spațiu de lucru Multi-AI / DBP București

**Statut:** STAGING / metodologie în lucru. Acest director nu este parte din aplicația publică.

## Scop
Pregătirea schimbului controlat de sarcini și rezultate pentru pilotul DBP Municipiul București, ocupația Electrician.

## Reguli
- `main` și aplicația de producție rămân nemodificate.
- Nu se încarcă în acest repository PUBLIC documente private Google Drive, date personale, parole, tokenuri sau chei API.
- DBP rămâne sursa de adevăr pentru date; GitHub ține codul, sarcinile și rezultatele tehnice.
- Mapările ESCO ↔ COR sunt doar candidate până la validare oficială.
- Fiecare rezultat indică sursă, versiune, dată și statut de validare.
- Nu se inițiază apeluri API cu plată, workflow-uri programate ori deployment fără aprobare explicită.
- Un răspuns AI nu este validare oficială și nu poate publica modificări automat.

## Flux propus (neactivat)
1. SOLON formulează sarcina după `task.schema.json`.
2. Un auditor tehnic extern poate produce un rezultat după `audit-result.schema.json` **numai printr-o integrare activată ulterior**.
3. SOLON verifică reproductibilitatea și proveniența.
4. Modificările de cod se propun prin branch/PR, cu aprobare umană.

**Situația actuală:** fără integrare automată Qwen, fără secrete, fără workflow activ.
