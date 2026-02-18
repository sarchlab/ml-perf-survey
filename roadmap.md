# Roadmap — ML Performance Survey Paper

**Last updated:** 2026-02-17 by Athena (Cycle 9)
**Target venue:** MICRO 2026
**Current state:** Paper at 1217 lines, ~13 body pages. Evaluation at ~50%. Must cut to 10.5-11 pages and add 3+ figures.

## Diagnosis

The human (issue #198) identified three critical requirements:
1. **Deep, surprising, controversial insights** — not a catalog
2. **At least 50% of paper weight on third-party evaluation with novel methodology**
3. **Guide future research** with concrete agendas

### Human Directives (Open)
- **#198**: Paper needs deep, controversial insights and 50% evaluation weight
- **#243**: No rubrics — evaluation must be accuracy-centered ✅ DONE
- **#244**: Evaluate ALL simulators + combine them for optimal solution ✅ DONE (5 tools evaluated, unified pipeline in Sec 8)
- **#246**: Discuss whether detailed NS-3-style network sim is needed ✅ DONE (Sec 8)
- **#250**: Define LLM-focused benchmark suite ✅ DONE (28-scenario suite in Sec 6)
- **#258**: Critical reviewer must review as hostile top-tier conference reviewer (skill rewritten, not yet executed)

## What M6a Accomplished (10 cycles)

- **PRs merged**: #274 (LLM benchmark suite) and #275 (network sim discussion) and #276 (methodology contribution) and #277 (evaluation expansion) all merged to main
- **Evaluation at ~50%**: Sections 6-7 span lines 434-1041 (608/1217 = 49.96%)
- **Methodology contribution articulated**: Accuracy-centered independent verification + LLM benchmark suite (Sec 1 intro)
- **91 references**: Exceeds 80+ target

### What M6a Did NOT Complete
- **Page count: FAIL** — body is ~13 pages (need 10.5-11). 2-2.5 pages over limit.
- **Figure count: FAIL** — only 5 figures (need 8+). Need 3+ more.
- **NeuSight mentions**: 61 times in paper. The ≤2 requirement from earlier milestones is unreasonable since NeuSight is one of 5 core evaluated tools. This requirement should be dropped.
- **Unified tool prototype**: Exists in `/prototype/` but not integrated into paper description.

### Lessons Learned
1. **Page limit ignored during content expansion** — adding 50% eval content pushed paper from 11 to 13 pages. Should have trimmed non-eval content simultaneously.
2. **Figures vs tables imbalance** — paper has 7 tables but only 5 figures. Some tables could be converted to figures for visual density AND space savings.
3. **Content compression must happen concurrently with expansion** — never expand one section without trimming another.
4. **NeuSight ≤2 requirement is incompatible** with NeuSight being a core evaluated tool. Dropping this constraint.

## Strategy (Revised)

The paper's evaluation content is solid at 50%. The remaining work is focused on presentation:
1. **Cut ~2.5 pages** of body content to reach 10.5-11 pages — compress non-evaluation sections (background, taxonomy, survey of approaches)
2. **Add 3+ figures** — convert some tables to figures, add architecture diagram for prototype
3. **Hostile critical review** per #258
4. **Integrate prototype description** into paper
5. **Final red team + polish**

## Milestones (Revised)

### M7: Paper Compression + Figure Expansion ← NEXT
Cut body content from ~13 to 10.5-11 pages while adding 3+ figures. This is primarily a presentation milestone.

**Specific targets:**
1. **Cut ~150-200 lines** from non-evaluation sections:
   - Background (Sec 3): compress standard ML background, keep only what's needed for survey context
   - Taxonomy (Sec 4): already compressed, may squeeze 10-20 more lines
   - Survey of Approaches (Sec 5): compress verbose tool descriptions into tighter summaries
   - Challenges/Future (Sec 9): trim speculation, keep concrete research agenda items
2. **Add 3+ figures** to reach 8 total:
   - Convert Table 2 (accuracy comparison) to a bar chart figure — more visual, saves space
   - Add architecture diagram for unified simulation pipeline (Sec 8)
   - Add coverage heatmap showing tool × workload coverage gaps
3. **Verify page count** reaches 10.5-11 pages body content
4. **Maintain 50% evaluation ratio** — cuts must come from non-eval sections

**Budget: 10 cycles**

### M7b: Hostile Critical Review + Fix Round
Fresh hostile review per #258, then fix all issues.
- **Budget: 10 cycles**

### M8: Unified Tool Prototype Integration
Describe prototype in paper, ensure it's a real contribution.
- **Budget: 10 cycles**

### M9: Red Team Review + Final Polish
Three-reviewer red team, fix issues, final PDF.
- **Budget: 10 cycles**

## Completed Milestones

- M1-M4: Literature discovery, taxonomy, deep analysis, paper draft
- M5: Fix reject-level issues — page limit, Pareto methodology, contribution framing
- M6 (partial): Evaluation restructuring — paper restructured, MTAP removed, accuracy-centered eval added, taxonomy compressed
- M6a (partial): PRs merged, eval at 50%, methodology contribution articulated. Failed page limit and figure count.

## Risk Assessment

- **Biggest risk:** Cutting 2.5 pages without losing evaluation content quality. Must be surgical — compress non-eval sections only.
- **Second risk:** Converting tables to figures may require TikZ/PGFplots work that is time-consuming.
- **Reduced risks:** Evaluation content is solid. References exceed target. Core structure is sound.
