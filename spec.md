# ML Performance Models Survey

## Goal

Write a paper for **MICRO 2026** that provides a systematic review of high-level ML performance models and simulators, **including third-party evaluation of key solutions**.

## Long-Term Vision

Beyond the survey paper, explore creating a unified performance modeling tool that combines the best approaches from literature—a practical contribution for the community.

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

### M5: Experimental Evaluation (Target: Week 14) ✅ COMPLETE
- Selected 5 tools: Timeloop, FlashAttention, ASTRA-sim, VIDUR, nn-Meter
- Evaluated reproducibility, usability, and accuracy validation
- Documented findings in data/evaluation/ directory
- Added Section 7 (Experimental Evaluation) to paper (PR #59)

### M6: Submission Ready (Target: Week 18) 🔄 IN PROGRESS
- **Convert to official MICRO 2026 LaTeX template** (11 pages, 9pt Times, 2-column) ✅ (PR #70 ready to merge)
- **Expand paper coverage** to address reviewer concerns ✅ (274 papers in database)
- **Address evaluation methodology criticism** - implement transparent rubric (issue #76 proposal)
- **Replace FlashAttention** in reproducibility section with ML-based predictor (e.g., NeuSight)
- **Clarify scope** - address ML-only vs mixed coverage confusion
- **Add quantitative synthesis** - normalized comparisons where feasible
- **Add visualization** - timeline, accuracy scatter plots, coverage heatmap
- Final polishing and formatting
- Camera-ready submission to MICRO 2026

### M7: Unified Tool Exploration (Post-Submission) 🆕
- Analyze feasibility of combining approaches
- Prototype unified performance modeling API
- If viable, develop open-source tool for community

## Current Status

**Active Milestone:** M6 - Submission Ready

**Progress:**
- Template conversion complete (PR #70 ready to merge)
- External reviewer feedback received (issues #69, #72) - two detailed reviews
- Paper database expanded to 274 papers (was ~60) - addresses coverage criticism
- Evaluation rubric proposed by Leo (issue #76) - pending team decision
- Merge conflicts resolved (issue #73 closed)

**Critical Reviewer Feedback (Both Reviews):**
1. Coverage was insufficient (~60 papers) - ADDRESSED (now 274)
2. Evaluation scores lack defined rubric - PROPOSED (issue #76)
3. Scope confusion: title says "ML" but includes non-ML tools - NEEDS DECISION
4. FlashAttention in reproducibility section is out of scope - NEEDS REPLACEMENT
5. Future directions too generic - NEEDS WORK
6. Missing quantitative meta-analysis - NEEDS WORK

**Next Steps:**
1. Merge PR #70 (template conversion)
2. Decide on evaluation methodology: rubric-based (Option A) or qualitative-only (Option B)
3. Replace FlashAttention with ML-based predictor in evaluation section
4. Clarify paper scope in abstract/introduction
5. Add additional figures for visual synthesis
6. Final page count verification (11 pages max)
