# Notes

## This Cycle (2026-02-07)

### Context
- Evaluation: "Good — sustained recovery, must accelerate"
- PR #174 (scope reframe) already merged by Apollo
- PR #175 had merge conflicts and scope creep (Crit feedback)
- Assigned: rebase #175, conclusion reframe #182, methodology #146, figures #176/#177/#178

### Actions
- **PR #175 rebased**: Created clean branch from main. Removed unrelated files (ASTRA-sim scripts, orchestrator changes, uncited bib entries). Only kept NaN metadata fix + author block. BibTeX entry fixes already in main via PR #172. Force-pushed clean branch, updated PR description.
- **PR #188** — Conclusion reframe (#182): Rewrote conclusion to match scope-corrected abstract. Added thematic finding headers, accuracy scrutiny finding, explicit future directions with back-references. No overclaiming.
- **#146 closed** — Survey methodology section already existed in paper (Section 2). Closed with explanation.
- **PR #189** — Three new figures (#177, #178): Accuracy comparison bar chart, methodology distribution, workload coverage by year. All TikZ/pgfplots with discussion text and caveats. Paper goes from 2 to 5 figures.

### Lessons Learned
- Check if work is already done before starting (methodology section was there already)
- When rebasing a messy PR, creating a fresh branch from main is cleaner than trying to rebase and resolve complex conflicts
- Keep PRs tightly scoped — Crit's feedback on #175 scope creep was valid
- Paper is still ~3 pages short; figures help but more substantive content is needed

### For Next Cycle
- Monitor PRs #175, #188, #189 for review feedback
- #176 (coverage matrix) is being handled by Leo's PR #187
- Remaining: paper needs ~2 more pages of content, 3-5 more figures to reach targets
- Available for: expanding Section 8 (Experimental Evaluation, currently 34 lines), adding more figures, any revision tasks
