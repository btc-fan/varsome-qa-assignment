# Assignment Audit — VarSome BRAF:V600E (local, gitignored)

## Spec coverage vs implementation

| Spec step / expected | Status |
|---|---|
| S1 launch + homepage | ✅ (search-bar label not asserted) |
| S2 type variant + verify genome=hg38 + Search | ✅ genome selected + asserted |
| S2 modal appears before results | ✅ |
| S3 Germline tab green | ✅ is_germline_tab_active() |
| S3 fill fields + leave others blank | ✅ (blanks not asserted empty) |
| S3 modal closes + redirect | ✅ wait_closed() |
| S4 sections GenInfo/Germline/PharmGKB/ClinVar/LOVD/Publications | ✅ all asserted |
| S5 expand + evidence rules visible | ⚠️ expands + waits header; evidence rules NOT asserted |
| S6 verdict "Pathogenic" red | ✅ text + red pill background |
| Objective: "expected SCORE and INTERPRETATION" | ❌ NOT verified |

## The real miss
Objective wants "Pathogenic, with the expected **score and interpretation**." We assert
verdict text + colour only. Live pill shows "13 points = 13P-0B" + ACMG rules (PP3, PM1…).
Add SCORE / INTERPRETATION / evidence-rule locators + assertions.

## Senior enhancements
High:
1. Score + interpretation assertions (+ assert S5 evidence rules).
2. Negative/discriminating test: a Benign variant → verdict != Pathogenic / not red.
   Proves the suite detects wrong verdicts (not always-green). Highest senior signal.
3. Robust verdict locator (prefer data-testid over styled-component class).
Medium:
4. Cross-browser (Firefox factory exists) — CI matrix chrome+firefox.
5. Richer failure evidence: attach page source + browser console/network logs.
6. Wait discipline: split fast interaction wait vs slower results-load wait.
Low:
7. Dead config: settings.genome unused (genome now per-scenario). Remove + .env GENOME row.
8. Assert S1 search-bar label + S3 blank fields stay empty (literal spec fidelity).
9. Login test: finish live-verification of selectors + creds.

## Blocked by live site (rate limit + reCAPTCHA) vs doable now
- Live-verify needed: 1, 2, 3, 8 (exact strings/behavior).
- Doable now: 4, 5, 6, 7.

## Order
1. Now: remove dead settings.genome; console/page-source capture on failure; Firefox CI matrix; split waits.
2. Build + verify later (account): score/interpretation/evidence assertions; negative Benign scenario; search-bar label.
