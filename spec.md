# A Survey of High-Level Modeling and Simulation Methods for Modern Machine Learning Workloads

## Goal

Write a paper for **MICRO 2026** that provides:
1. A systematic survey on performance modeling and simulation for ML workloads with a novel taxonomy
2. Third-party evaluation of tools using common benchmarks (run by us)
3. A new unified tool that combines the best approaches

## Paper Contributions

### Contribution 1: Systematic Survey with Taxonomy
- Comprehensive literature review of performance modeling and simulation methods for ML workloads
- Novel taxonomy that classifies approaches by methodology, target hardware, and workload coverage
- Identification of gaps and trends in the field

### Contribution 2: Third-Party Evaluation
- Define common benchmark suite for fair comparison across tool categories
- Execute all tools ourselves on the same benchmarks
- Evaluate on multiple dimensions: **accuracy**, **ease of use**, **performance**, and **extensibility**
- Report which tools excel and which fall short, with quantitative results

### Contribution 3: Unified Tool (ZZZ)
- Combine best methods from each category into a new unified tool
- Target: outperform existing tools on key metrics
- Open-source contribution for the community

## Milestones

### M1: Literature Discovery (Target: Week 2) ✅ COMPLETE
- Identify relevant papers on ML performance models and simulators
- Create a structured bibliography database
- Categorize papers by approach (analytical, simulation, hybrid, ML-based)

### M2: Taxonomy Development (Target: Week 4) ✅ COMPLETE
- Define classification dimensions (accuracy, speed, target hardware, etc.)
- Create comparison framework
- Draft taxonomy section of paper

### M3: Deep Analysis (Target: Week 8) ✅ COMPLETE
- Detailed review of key papers in each category
- Extract methodology patterns
- Identify gaps and opportunities

### M4: Paper Draft (Target: Week 12) ✅ COMPLETE
- Complete first draft of all sections
- Generate comparison tables and figures
- Internal review and revision

### M5: Preliminary Evaluation (Target: Week 14) ✅ COMPLETE
- Initial tool evaluations (Timeloop, ASTRA-sim, VIDUR, nn-Meter, etc.)
- Documented findings in data/evaluation/ directory
- Added Section 7 (Experimental Evaluation) to paper

### M6: Benchmark Definition (Target: Week 18) 🔄 IN PROGRESS
- Define common benchmark suite across tool categories
- Select representative ML workloads (CNN, Transformer, LLM, etc.)
- Define evaluation metrics: accuracy (vs. real hardware), latency, memory, ease of use, extensibility
- Document benchmark methodology for reproducibility

### M7: Comprehensive Third-Party Evaluation (Target: Week 22) 🆕
- Execute all selected tools on common benchmarks
- Collect quantitative results across all evaluation dimensions
- Identify winners and losers for each metric
- Generate comparison tables and figures

### M8: Unified Tool Development (Target: Week 28) 🆕
- Analyze best-performing approaches from each category
- Design unified architecture combining strengths
- Implement prototype of unified tool
- Validate against benchmark suite

### M9: Submission Ready (Target: Week 32) 🆕
- Complete paper with all three contributions
- Quantitative comparisons: "ZZZ outperforms X by Y% on metric Z"
- Final polishing and formatting
- Camera-ready submission to MICRO 2026

## Current Status

**Active Milestone:** M6 - Benchmark Definition

**What's Changed:**
- Human direction received (issue #86): Paper scope expanded to include unified tool development
- Title corrected (issue #89): Now focuses on "ML Workloads" not "ML Approaches"
- Previous M6 work (template conversion, scope clarification) carries forward

**Carry-Forward Progress:**
- Template conversion complete (PR #70 ready to merge)
- Paper database: 274 papers catalogued
- Initial evaluations completed (5 tools)
- Multiple open PRs addressing prior feedback (#84, #85, #87, #88)

**Next Steps:**
1. Merge outstanding PRs (#70, #84, #85, #87, #88)
2. Define common benchmark suite
3. Select final tool set for comprehensive evaluation
4. Begin benchmark execution
