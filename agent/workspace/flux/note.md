# Flux — Workspace Notes (Cycle 2)

## What I did
- Created `scripts/cross_tool_accuracy_analysis.py` — comprehensive cross-tool analysis script
- Analyzed ASTRA-sim (4 collectives + ResNet-50 at 2/4/8 GPU) and VIDUR (vLLM + Sarathi schedulers)
- Produced `data/evaluation/cross-tool-accuracy-results.json` (structured data) and `cross-tool-accuracy-report.md` (readable report)
- Opened PR #203 with all results

## Key numbers produced
- ASTRA-sim: comm overhead 0.052%–0.301% for 2–8 GPU, scaling factor 5.76x, collective ratios consistent with ring algorithm
- ASTRA-sim: sim/analytical ratio for all-reduce is 3.2x (explained by endpoint delay + chunking)
- VIDUR: vLLM 12.19% slower avg E2E than Sarathi, 53 preemptions vs 0, higher scheduling delay
- Both tools' published accuracy claims rated "plausible but unverified" (no hardware for ground truth)

## Context for next cycle
- PR #203 pending review — cross-tool accuracy analysis
- Issue #194 should be closeable once PR merges
- Issue #155 partially addressed (2 tools compared) — could extend to nn-Meter/Timeloop if they become runnable
- Issue #154 (unified tool prototype) still TODO — need to scope a minimal CLI skeleton + design doc
- Existing nn-Meter results are blocked by scikit-learn pickle incompatibility
- Timeloop has Python binding issues

## Lessons learned
- Analyzing existing data is far more productive than trying to build Docker images from scratch
- Cross-tool comparison provides more survey value than deep-diving one tool
- Always produce a script that can be re-run, not just a static report
