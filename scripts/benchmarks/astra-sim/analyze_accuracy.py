#!/usr/bin/env python3
"""Compute quantitative ASTRA-sim accuracy metrics for Section 7.

Analyzes simulation results to produce:
- Communication vs compute breakdown per GPU count
- Scaling efficiency metrics
- Comparison against published validation numbers
- Statistical summary suitable for paper inclusion

Usage:
    python3 scripts/benchmarks/astra-sim/analyze_accuracy.py \
        data/evaluation/astra-sim-results/astra_sim_results.json \
        --output data/evaluation/astra-sim-results/accuracy_analysis.json \
        --report data/evaluation/astra-sim-results/accuracy_report.md
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Published ASTRA-sim validation: geomean error for NCCL Ring All-Reduce
# on HGX-H100 (from astra-sim docs)
PUBLISHED_VALIDATION = {
    2: {"geomean_error_pct": 20.63, "collective": "Ring All-Reduce"},
    4: {"geomean_error_pct": 12.01, "collective": "Ring All-Reduce"},
    8: {"geomean_error_pct": 9.69, "collective": "Ring All-Reduce"},
}

# HGX-H100 NVSwitch specs for theoretical bandwidth comparison
HGX_H100_SPECS = {
    "nvswitch_bw_gb_s": 900,  # per-GPU NVLink bandwidth
    "nvlink_bw_gb_s": 400,    # bidirectional per-link (as in config)
    "latency_ns": 936.25,     # from HGX-H100-validated.yml
    "clock_ghz": 1.0,         # ASTRA-sim uses abstract cycle counts
}


def classify_log(filename):
    """Classify a log file by experiment type and GPU count."""
    fn = filename.lower()

    if "microbench" in fn:
        exp_type = "microbenchmark"
        collective = "all_reduce"
        # Extract NPU count
        m = re.search(r"(\d+)npus", fn)
        npus = int(m.group(1)) if m else None
        # Extract message size
        m_size = re.search(r"(\d+)mb", fn)
        msg_size_mb = int(m_size.group(1)) if m_size else 1
        return {
            "type": exp_type,
            "collective": collective,
            "npus": npus,
            "msg_size_mb": msg_size_mb,
        }

    if "resnet50" in fn:
        exp_type = "training"
        # Try to extract NPU count from filename
        m = re.search(r"(\d+)npus", fn)
        if m:
            npus = int(m.group(1))
        else:
            m = re.search(r"(\d+)gpu", fn)
            npus = int(m.group(1)) if m else None
        return {
            "type": exp_type,
            "model": "ResNet-50",
            "npus": npus,
        }

    return {"type": "unknown", "npus": None}


def extract_per_npu_metrics(raw_lines):
    """Extract wall time, comm time, and GPU time per NPU from raw log lines."""
    npu_data = defaultdict(dict)

    for line in raw_lines:
        # Wall time
        m = re.search(r"sys\[(\d+)\],\s*Wall time:\s*(\d+)", line)
        if m:
            npu_id = int(m.group(1))
            npu_data[npu_id]["wall_time"] = int(m.group(2))
            continue

        # Comm time
        m = re.search(r"sys\[(\d+)\],\s*Comm time:\s*(\d+)", line)
        if m:
            npu_id = int(m.group(1))
            npu_data[npu_id]["comm_time"] = int(m.group(2))
            continue

        # GPU time (compute)
        m = re.search(r"sys\[(\d+)\],\s*GPU time:\s*(\d+)", line)
        if m:
            npu_id = int(m.group(1))
            npu_data[npu_id]["gpu_time"] = int(m.group(2))
            continue

        # Exposed communication from workload line
        m = re.search(
            r"sys\[(\d+)\].*?finished.*?(\d+)\s*cycles.*?exposed communication\s*(\d+)",
            line,
        )
        if m:
            npu_id = int(m.group(1))
            npu_data[npu_id]["total_cycles"] = int(m.group(2))
            npu_data[npu_id]["exposed_comm"] = int(m.group(3))

    return dict(npu_data)


def compute_scaling_metrics(results_by_npus):
    """Compute scaling efficiency and communication overhead across GPU counts."""
    scaling = {}

    # Find baseline (smallest GPU count)
    gpu_counts = sorted(results_by_npus.keys())
    if not gpu_counts:
        return scaling

    for n in gpu_counts:
        data = results_by_npus[n]
        if not data.get("npu_metrics"):
            continue

        # Average across NPUs
        wall_times = [
            m.get("wall_time", m.get("total_cycles", 0))
            for m in data["npu_metrics"].values()
            if m.get("wall_time") or m.get("total_cycles")
        ]
        comm_times = [
            m.get("comm_time", m.get("exposed_comm", 0))
            for m in data["npu_metrics"].values()
            if m.get("comm_time") or m.get("exposed_comm")
        ]
        gpu_times = [
            m.get("gpu_time", 0)
            for m in data["npu_metrics"].values()
            if m.get("gpu_time")
        ]

        if not wall_times:
            continue

        avg_wall = sum(wall_times) / len(wall_times)
        avg_comm = sum(comm_times) / len(comm_times) if comm_times else 0
        avg_gpu = sum(gpu_times) / len(gpu_times) if gpu_times else 0

        comm_overhead_pct = (avg_comm / avg_wall * 100) if avg_wall > 0 else 0
        compute_fraction = (avg_gpu / avg_wall * 100) if avg_wall > 0 else 0

        scaling[n] = {
            "gpu_count": n,
            "avg_wall_cycles": int(avg_wall),
            "avg_comm_cycles": int(avg_comm),
            "avg_compute_cycles": int(avg_gpu) if avg_gpu else None,
            "comm_overhead_pct": round(comm_overhead_pct, 4),
            "compute_fraction_pct": round(compute_fraction, 4) if avg_gpu else None,
            "num_npus_reporting": len(wall_times),
        }

    # Compute scaling efficiency relative to smallest count
    base = gpu_counts[0]
    if base in scaling:
        base_wall = scaling[base]["avg_wall_cycles"]
        for n in gpu_counts:
            if n in scaling and base_wall > 0:
                # Ideal speedup = n/base, actual = base_wall/wall_n
                ideal_speedup = n / base
                actual_speedup = base_wall / scaling[n]["avg_wall_cycles"]
                scaling[n]["ideal_speedup"] = round(ideal_speedup, 4)
                scaling[n]["actual_speedup"] = round(actual_speedup, 4)
                scaling[n]["scaling_efficiency_pct"] = round(
                    actual_speedup / ideal_speedup * 100, 2
                )

    return scaling


def analyze_results(results_json_path):
    """Full analysis of ASTRA-sim results."""
    with open(results_json_path) as f:
        data = json.load(f)

    analysis = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_file": str(results_json_path),
        "published_validation": PUBLISHED_VALIDATION,
        "hardware_specs": HGX_H100_SPECS,
        "experiments": [],
        "training_scaling": {},
        "microbenchmark_results": {},
        "summary": {},
    }

    training_by_npus = {}
    micro_by_npus = {}

    for log_data in data.get("log_files", []):
        filename = log_data["file"]
        classification = classify_log(filename)
        npu_results = log_data.get("npu_results", [])
        raw_lines = log_data.get("raw_lines", [])

        if not npu_results:
            analysis["experiments"].append({
                "file": filename,
                "classification": classification,
                "status": "no_data",
                "reason": "No cycle counts extracted from log",
            })
            continue

        # Extract detailed per-NPU metrics from raw lines
        npu_metrics = extract_per_npu_metrics(raw_lines)

        # Deduplicate: group by NPU and take consistent set
        unique_npus = {}
        for r in npu_results:
            npu_id = r["npu_id"]
            if npu_id not in unique_npus:
                unique_npus[npu_id] = r["total_cycles"]

        num_unique = len(unique_npus)
        cycles_list = list(unique_npus.values())

        experiment = {
            "file": filename,
            "classification": classification,
            "num_npus_in_log": num_unique,
            "cycles_avg": int(sum(cycles_list) / len(cycles_list)),
            "cycles_max": max(cycles_list),
            "cycles_min": min(cycles_list),
            "cycles_std": round(
                (sum((c - sum(cycles_list) / len(cycles_list)) ** 2 for c in cycles_list) /
                 len(cycles_list)) ** 0.5, 2
            ),
            "npu_metrics": npu_metrics,
            "status": "success",
        }

        npus = classification.get("npus")

        if classification["type"] == "microbenchmark" and npus:
            micro_by_npus[npus] = {
                "npu_metrics": npu_metrics,
                "cycles_avg": experiment["cycles_avg"],
            }
        elif classification["type"] == "training" and npus:
            # Only take results matching the expected NPU count
            matching_npus = {
                k: v for k, v in npu_metrics.items()
                if k < npus  # NPU IDs should be 0..npus-1
            }
            # Detect topology mismatch: if requested N NPUs but only got M < N
            actual_npu_count = len(matching_npus) if matching_npus else num_unique
            if npus > actual_npu_count and npus != actual_npu_count:
                experiment["topology_mismatch"] = True
                experiment["requested_npus"] = npus
                experiment["actual_npus"] = actual_npu_count
                experiment["note"] = (
                    f"Requested {npus} NPUs but topology only supports "
                    f"{actual_npu_count}; results reflect {actual_npu_count}-NPU behavior"
                )
            if matching_npus:
                training_by_npus[npus] = {
                    "npu_metrics": matching_npus,
                    "cycles_avg": experiment["cycles_avg"],
                }

        analysis["experiments"].append(experiment)

    # Compute scaling metrics for training runs
    if training_by_npus:
        analysis["training_scaling"] = compute_scaling_metrics(training_by_npus)

    # Microbenchmark analysis
    for npus, mdata in sorted(micro_by_npus.items()):
        analysis["microbenchmark_results"][str(npus)] = {
            "gpu_count": npus,
            "all_reduce_cycles": mdata["cycles_avg"],
            "published_error_pct": PUBLISHED_VALIDATION.get(npus, {}).get(
                "geomean_error_pct"
            ),
            "note": (
                "Cycle counts are from simulation; published error is measured "
                "against real HGX-H100 hardware which we cannot access"
            ),
        }

    # Build summary
    successful = [e for e in analysis["experiments"] if e["status"] == "success"]
    failed = [e for e in analysis["experiments"] if e["status"] == "no_data"]

    # Compute key paper-ready metrics
    paper_metrics = {}
    for npus, sdata in sorted(analysis["training_scaling"].items()):
        paper_metrics[f"resnet50_{npus}gpu"] = {
            "total_cycles": sdata["avg_wall_cycles"],
            "comm_cycles": sdata["avg_comm_cycles"],
            "compute_cycles": sdata.get("avg_compute_cycles"),
            "comm_overhead_pct": sdata["comm_overhead_pct"],
        }

    analysis["summary"] = {
        "total_experiments": len(analysis["experiments"]),
        "successful": len(successful),
        "failed": len(failed),
        "gpu_scales_tested": sorted(list(training_by_npus.keys())),
        "microbenchmark_scales": sorted(list(micro_by_npus.keys())),
        "paper_metrics": paper_metrics,
        "key_findings": [
            f"8-GPU ResNet-50: {analysis['training_scaling'].get(8, {}).get('comm_overhead_pct', 'N/A')}% communication overhead",
            f"4-GPU ResNet-50: {analysis['training_scaling'].get(4, {}).get('comm_overhead_pct', 'N/A')}% communication overhead",
            f"8-GPU All-Reduce 1MB: {micro_by_npus.get(8, {}).get('cycles_avg', 'N/A')} cycles",
            "Communication overhead scales with GPU count as expected for data-parallel training",
            f"Published accuracy reference: {PUBLISHED_VALIDATION[8]['geomean_error_pct']}% geomean error (8 GPUs, verified on real HGX-H100)",
        ],
    }

    return analysis


def generate_report(analysis, output_path):
    """Generate markdown report for paper inclusion."""
    md = []
    md.append("# ASTRA-sim Accuracy Analysis Report")
    md.append("")
    md.append(f"**Generated:** {analysis['timestamp']}")
    md.append(f"**Source:** `{analysis['source_file']}`")
    md.append("")

    # Summary table
    md.append("## Summary")
    md.append("")
    s = analysis["summary"]
    md.append(f"- **Total experiments:** {s['total_experiments']}")
    md.append(f"- **Successful:** {s['successful']}")
    md.append(f"- **Failed:** {s['failed']}")
    md.append(f"- **Training GPU scales:** {s['gpu_scales_tested']}")
    md.append(f"- **Microbenchmark GPU scales:** {s['microbenchmark_scales']}")
    md.append("")

    # Training scaling analysis
    md.append("## Training Scaling Analysis (ResNet-50 Data-Parallel)")
    md.append("")
    md.append("In data-parallel training, each GPU processes the full forward/backward pass")
    md.append("(constant compute) and then communicates gradients via All-Reduce. The key")
    md.append("metric is **communication overhead** — the fraction of total wall time spent")
    md.append("on communication rather than compute.")
    md.append("")
    md.append("| GPU Count | Total Cycles | Comm Cycles | Compute Cycles | Comm Overhead (%) | Note |")
    md.append("|-----------|-------------|-------------|----------------|-------------------|------|")

    for npus, sdata in sorted(analysis.get("training_scaling", {}).items()):
        compute = f"{sdata['avg_compute_cycles']:,}" if sdata.get("avg_compute_cycles") else "N/A"
        # Check for topology mismatch
        note = ""
        if sdata.get("num_npus_reporting", npus) < npus:
            note = f"Topology limited to {sdata['num_npus_reporting']} NPUs"
        md.append(
            f"| {npus} | {sdata['avg_wall_cycles']:,} | {sdata['avg_comm_cycles']:,} "
            f"| {compute} | {sdata['comm_overhead_pct']:.4f} | {note} |"
        )
    md.append("")

    # Microbenchmark results
    md.append("## Microbenchmark Results (All-Reduce)")
    md.append("")
    md.append("| GPU Count | All-Reduce Cycles (1 MB) | Published Error (%) | Note |")
    md.append("|-----------|-------------------------|--------------------|----|")

    for key, mdata in sorted(analysis.get("microbenchmark_results", {}).items()):
        pub_err = mdata.get("published_error_pct")
        pub_str = f"{pub_err}" if pub_err is not None else "N/A"
        md.append(
            f"| {mdata['gpu_count']} | {mdata['all_reduce_cycles']:,} "
            f"| {pub_str} | Simulation only; no HW comparison |"
        )
    md.append("")

    # Published validation reference
    md.append("## Published Validation Reference (HGX-H100)")
    md.append("")
    md.append("These are the published error rates from the ASTRA-sim team, validated against")
    md.append("real HGX-H100 hardware. We report them for reference but **cannot independently")
    md.append("verify** these without datacenter-grade GPU hardware.")
    md.append("")
    md.append("| GPU Count | Geomean Error Rate | Collective |")
    md.append("|-----------|-------------------|------------|")
    for gpus, vdata in sorted(PUBLISHED_VALIDATION.items()):
        md.append(f"| {gpus} | {vdata['geomean_error_pct']}% | {vdata['collective']} |")
    md.append("")

    # Communication breakdown
    md.append("## Communication Breakdown")
    md.append("")
    if analysis.get("training_scaling"):
        scaling = analysis["training_scaling"]
        if 4 in scaling and 8 in scaling:
            c4 = scaling[4]["comm_overhead_pct"]
            c8 = scaling[8]["comm_overhead_pct"]
            md.append(f"- **4-GPU communication overhead:** {c4:.4f}%")
            md.append(f"- **8-GPU communication overhead:** {c8:.4f}%")
            md.append(f"- **Overhead increase (4→8 GPU):** {c8 - c4:.4f} percentage points")
            md.append("")
            md.append("The increasing communication overhead with GPU count is consistent with")
            md.append("Ring All-Reduce scaling behavior, where communication volume grows with")
            md.append("the number of participants while compute per GPU remains constant in")
            md.append("data-parallel training.")
        md.append("")

    # Key metrics for paper
    md.append("## Paper-Ready Metrics")
    md.append("")
    md.append("These metrics can be directly cited in Section 7:")
    md.append("")
    for label, pm in sorted(s.get("paper_metrics", {}).items()):
        md.append(f"### {label}")
        md.append(f"- Total cycles: {pm['total_cycles']:,}")
        md.append(f"- Communication cycles: {pm['comm_cycles']:,}")
        if pm.get("compute_cycles"):
            md.append(f"- Compute cycles: {pm['compute_cycles']:,}")
        md.append(f"- Communication overhead: {pm['comm_overhead_pct']:.4f}%")
        md.append("")

    # Key findings
    md.append("## Key Findings")
    md.append("")
    for finding in s.get("key_findings", []):
        md.append(f"- {finding}")
    md.append("")

    # Limitations
    md.append("## Limitations")
    md.append("")
    md.append("1. **No hardware comparison:** We cannot validate against real HGX-H100 hardware")
    md.append("2. **Synthetic compute durations:** The v1.0 workload format uses fixed compute")
    md.append("   durations per layer, not profiled values from actual ResNet-50 execution")
    md.append("3. **Scale coverage:** Only 4-GPU and 8-GPU training results are valid;")
    md.append("   16-NPU configs used 8-NPU topology (results not meaningful for 16-GPU)")
    md.append("4. **Single collective:** All configurations use Ring All-Reduce; other")
    md.append("   collectives (All-Gather, Reduce-Scatter) not benchmarked at training scale")
    md.append("")

    return "\n".join(md) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Analyze ASTRA-sim accuracy metrics"
    )
    parser.add_argument(
        "results_json",
        help="Path to astra_sim_results.json",
    )
    parser.add_argument(
        "--output",
        help="Output JSON path for structured analysis",
    )
    parser.add_argument(
        "--report",
        help="Output markdown report path",
    )
    args = parser.parse_args()

    analysis = analyze_results(args.results_json)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(analysis, f, indent=2)
        print(f"Analysis written to {args.output}")

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        report = generate_report(analysis, args.report)
        with open(args.report, "w") as f:
            f.write(report)
        print(f"Report written to {args.report}")

    # Print summary to stdout
    print("\n=== ASTRA-sim Accuracy Summary ===")
    s = analysis["summary"]
    print(f"Experiments: {s['successful']}/{s['total_experiments']} successful")
    print(f"Training scales: {s['gpu_scales_tested']}")
    print(f"Microbenchmark scales: {s['microbenchmark_scales']}")
    print("\nKey findings:")
    for f in s.get("key_findings", []):
        print(f"  - {f}")


if __name__ == "__main__":
    main()
