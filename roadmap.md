# Roadmap — ML Performance Survey Paper

**Last updated:** 2026-02-20 by Athena (Cycle 14 — M11 complete, defining M12)
**Target venue:** MICRO 2026
**Current state:** Paper at ~1120 lines, 15 pages, 9 figures, 101 refs. M11 complete: within-category comparisons in 4 categories, H100 data integrated, no regressions. Apollo verified (Elena 4/4, Raj 9/9). Ready for final red team and submission polish.

## What's Done (M1–M11)

- **M1-M4**: Literature, taxonomy, deep analysis, paper draft
- **M5-M8**: Fix rounds, evaluation restructuring, compression, hostile review
- **M9**: GPU scripts, 10 tools evaluated (5 full + 5 deployment), PerfSim-Survey-2026 benchmark (36 scenarios), multi-backend scripts
- **M10**: Paper expanded to 10 content pages, 8 figures, 98 refs. 3-reviewer red team ran, all findings fixed, 7/7 pass.
- **M11**: Within-category comparative evaluation (4 categories, 2+ tools each), H100 ground-truth integration (33/36 scenarios), self-reported vs third-party accuracy figure, 3 new comparison tables (kernel, distributed, inference), Paleo + TrioSim added. Paper now 15 pages, 9 figures, 101 refs.

### Key Findings
- Self-reported accuracy unreliable (NeuSight 2.3% claimed vs 8.74% measured on H100)
- Composition gap (5–9% kernel → 10–28% model error) dominates total error
- nn-Meter fails due to dependency rot
- 56% of PerfSim-Survey-2026 scenarios lack tool support (20/36)
- Tools are complementary, not competing
- H100 ground-truth validates accuracy overstatement pattern

### Human Directives Status
- **#36** (comparative eval): ✅ DONE — 4 categories with 2+ tools
- **#35** (H100 results): ✅ DONE — integrated with validation subsection
- **#37** (page limit relaxed): ✅ DONE — 15 pages, concise writing
- **#3** (original suggestions): Mostly addressed. Remaining minor items: background section length, figure text readability, benchmark parameter table format, supplementary materials preparation

## Remaining Milestones

### M11: Comparative Tool Evaluation + H100 Integration ✅ COMPLETE
Elena verified 4/4 within-category criteria. Raj verified 9/9 quantitative criteria. No regressions.

### M12: Final Red Team Review + Submission Polish (10 cycles) ← NEXT

This is the final milestone before submission. Two parallel tracks:

**Track A: Red Team Review (fresh, independent per #195)**
1. **Hostile reviewer** — fresh MICRO PC review, no memory of prior reviews. Score the paper 1-6, identify top weaknesses.
2. **Paragraph reviewer** — line-by-line review checking: unsupported claims, logical gaps, numerical errors, writing quality.
3. **Comparative reviewer** — compare against 2-3 top-tier MICRO/ISCA survey papers. Identify structural and depth gaps.

**Track B: Remaining Polish (from #3 and general assessment)**
1. **Figure readability**: Check all figures for text size issues. Human specifically complained about text being too small (#3.5). Ensure figure text is comparable to main text size.
2. **Background section**: Currently only 2 lines (#3.4). Either expand to useful length or remove entirely — 2 lines adds no value.
3. **Benchmark parameter table**: Consider replacing "Concrete benchmark parameterization" paragraph with a comprehensive table (#3.13).
4. **Numerical accuracy**: Verify Felix's M10 findings were fixed (VIDUR 12.2% → actual 10.7%, GPU count inconsistency, ASTRA-sim scaling claim).

**Track C: Fix Round**
After red team reports, fix all findings. Then verify fixes.

**Pass/fail for Apollo (M12):**
- Red team hostile reviewer scores ≥4/6 (Weak Accept or better)
- All numerical claims verified — no unsupported numbers
- No figure readability issues — all figure text at readable size
- No overclaims, no TODOs, no broken references
- All #3 items either addressed or explicitly out of scope with justification
- Paper compiles cleanly with no warnings

### Post-M12: Submission Preparation
- Prepare supplementary materials package (scripts, configs, Docker files)
- Final PDF build and review
- Submit to MICRO 2026

## Lessons Learned

1. **Page count**: Use PDF analysis (pdfinfo), not line count. Distinguish content pages from reference pages.
2. **Verification scope**: Apollo criteria must be concrete and measurable. Subjective criteria cause endless fix rounds.
3. **Fix round discipline**: M7 burned 30 cycles; M9 had 4 verification passes. Set clear pass/fail and stick to it.
4. **Worker timeouts**: One task per worker per cycle. Keep tasks focused.
5. **Prototype gap**: Code was written but never discussed in paper — always ensure implementation work appears in manuscript.
6. **Compression danger**: M7's compression from 907→715 lines lost 3 pages of content. Don't compress below the page limit.
7. **Script portability**: Always test scripts on multiple GPU backends from the start.
8. **Evaluation breadth matters**: Within-category comparison is essential for a survey paper.
9. **M11 efficiency**: Parallel worker execution (Maya research → Leo integration) completed M11 in ~3 cycles. Use this pattern again.

## Risk Assessment

- **Top risk (M12)**: Red team finds deep structural issues requiring significant rewrite. Mitigation: 10 cycles budgeted; if hostile score is ≤2/6, escalate to Athena for re-scoping.
- **Medium risk**: Figure readability fixes break layout or page flow. Mitigation: Make minimal changes, test PDF after each fix.
- **Low risk**: Numerical verification uncovers data errors requiring table rebuilds. Mitigation: Source data is well-documented in worker workspaces.
