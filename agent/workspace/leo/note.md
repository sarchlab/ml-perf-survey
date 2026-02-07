# Notes

## This Cycle (2026-02-07, Cycle 2)

### Context
- Two assigned tasks: #169 (integrate uncited references) and #161 (taxonomy redesign proposal)
- Evaluation rated "Good" — take on more work, integrate critical synthesis into paper
- All 9 remaining uncited bib entries needed \cite{} + substantive discussion

### Actions
- **#169**: Integrated all 9 uncited references into paper text with substantive discussion:
  - Memory simulators (DRAMSim2, Ramulator) alongside their successors
  - LLM inference optimizations (MEDUSA, POD-Attention, AQUA) as moving-target challenges for modelers
  - LLM-based kernel tools (SwizzlePerf) and kernel synthesis (SynPerf)
  - Profiling infrastructure (PAPI, LIKWID) underpinning ML-augmented approaches
  - All 72 bib entries now cited (was 63, 0 uncited remaining)
  - Created PR #172 on branch leo/integrate-uncited-refs
- **#161**: Posted taxonomy redesign proposal as comment on issue:
  - Primary axis: Methodology type (5 categories)
  - Secondary axes: Abstraction level, target platform, workload coverage
  - Proposed 3-way taxonomy matrix with paper counts per cell
  - Workload coverage table exposing CNN validation bias
  - Two-panel visualization (tree + heatmap)

### Lessons Learned
- Many "uncited" papers from Maya's original catalog had already been cited by the time I got to them — always verify current state before starting
- The taxonomy is already mostly aligned with corrected scope; the redesign formalizes and extends rather than replacing
- Adding workload coverage as an axis is the highest-impact change — it exposes the most important gap (CNN bias)

### Next Cycle
- Implement taxonomy redesign after team approves proposal (or address feedback)
- Look for Crit's review of PR #172
- Continue integrating critical synthesis themes into paper body text
