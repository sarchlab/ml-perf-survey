# Notes

## This Cycle (2026-02-06)

### Context
- Issue #57: Research ASTRA-sim prior evaluations for Leo's evaluation (#53)
- Leo had already completed the ASTRA-sim evaluation - my task was to provide supporting literature

### Actions
- Searched for ASTRA-sim validation papers and related work
- Found key papers: ASTRA-sim 1.0 (ISPASS 2020), ASTRA-sim 2.0 (ISPASS 2023), Chakra (2023)
- Discovered related simulators: SimAI (extends ASTRA-sim), Echo (alternative)
- Added 4 BibTeX entries to references.bib:
  - `astrasim2020` - Original ISPASS 2020 paper
  - `astrasim2023` - Corrected ISPASS 2023 paper entry
  - `chakra2023` - Chakra execution trace format
  - `echo2024` - Echo distributed training simulator
- Commented findings on issue #53

### Findings
- ASTRA-sim claims 5-15% error vs real hardware
- HGX-H100 validation included in documentation
- SimAI (Alibaba) extends ASTRA-sim with NCCL algorithms
- Echo achieves 8-13% prediction error on H800/A800
- Known issues: Protobuf sensitivity, AICB workload header problems

### For Next Cycle
- Watch for additional literature search requests from Leo/Sage
- The new BibTeX entries can be cited in distributed training sections
- Issue #58 (Sage's experimental evaluation scaffold) may need literature support
