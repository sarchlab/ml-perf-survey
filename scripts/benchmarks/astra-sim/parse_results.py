#!/usr/bin/env python3
"""Parse ASTRA-sim simulation output logs into structured results.

Extracts cycle counts, communication metrics, and computes accuracy
comparisons against published validation numbers.

Usage:
    python3 scripts/benchmarks/astra-sim/parse_results.py <results_dir>

For ML Performance Survey - Issue #170
Author: Flux (Tool Engineer)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# Published ASTRA-sim validation numbers (from official docs)
# https://astra-sim.github.io/astra-sim-docs/validation/hardware/gpu-validation-hgx-h100.html
PUBLISHED_VALIDATION = {
    "hgx-h100": {
        2: {"geomean_error_pct": 20.63},
        4: {"geomean_error_pct": 12.01},
        8: {"geomean_error_pct": 9.69},
    }
}


def parse_log_file(filepath: str) -> dict:
    """Extract metrics from an ASTRA-sim log file.

    Looks for patterns like:
    - sys[X] finished, <N> cycles
    - total exposed communication: <N>
    - total training time: <N>
    """
    metrics = {
        "file": os.path.basename(filepath),
        "npu_results": [],
        "raw_lines": [],
    }

    try:
        with open(filepath) as f:
            lines = f.readlines()
    except OSError as e:
        metrics["error"] = str(e)
        return metrics

    for line in lines:
        line = line.strip()

        # Match "sys[N] finished, <cycles> cycles" or similar
        m = re.search(
            r"sys\[(\d+)\].*?finished.*?(\d[\d,]*)\s*cycles?",
            line,
            re.IGNORECASE,
        )
        if m:
            npu_id = int(m.group(1))
            cycles = int(m.group(2).replace(",", ""))
            metrics["npu_results"].append({"npu_id": npu_id, "total_cycles": cycles})
            metrics["raw_lines"].append(line)
            continue

        # Match total/exposed communication
        m = re.search(
            r"(total|exposed)\s+(communication|comm).*?(\d[\d,]*)",
            line,
            re.IGNORECASE,
        )
        if m:
            metrics["raw_lines"].append(line)
            continue

        # Match any line with "tick" or "latency" or "time"
        if re.search(r"(tick|latency|time|cycle)", line, re.IGNORECASE):
            if any(c.isdigit() for c in line):
                metrics["raw_lines"].append(line)

    return metrics


def summarize_results(results_dir: str) -> dict:
    """Parse all log files in a results directory."""
    results_dir = Path(results_dir)
    summary = {
        "results_dir": str(results_dir),
        "log_files": [],
        "published_validation": PUBLISHED_VALIDATION,
    }

    log_files = sorted(results_dir.glob("*.log"))
    if not log_files:
        summary["error"] = f"No .log files found in {results_dir}"
        return summary

    for log_file in log_files:
        if log_file.name in ("orchestrator.log", "docker_build.log"):
            continue
        parsed = parse_log_file(str(log_file))
        summary["log_files"].append(parsed)

    return summary


def print_summary(summary: dict) -> None:
    """Print human-readable summary."""
    print("=" * 60)
    print("ASTRA-sim Results Summary")
    print("=" * 60)
    print(f"Results directory: {summary['results_dir']}")
    print()

    if "error" in summary:
        print(f"ERROR: {summary['error']}")
        return

    for log_data in summary["log_files"]:
        print(f"--- {log_data['file']} ---")
        if "error" in log_data:
            print(f"  Error: {log_data['error']}")
            continue

        if log_data["npu_results"]:
            for npu in log_data["npu_results"]:
                print(f"  NPU {npu['npu_id']}: {npu['total_cycles']:,} cycles")

            cycles_list = [n["total_cycles"] for n in log_data["npu_results"]]
            if cycles_list:
                avg = sum(cycles_list) / len(cycles_list)
                print(f"  Average: {avg:,.0f} cycles")
                print(f"  Max: {max(cycles_list):,} cycles")
                print(f"  Min: {min(cycles_list):,} cycles")
        else:
            print("  No cycle counts extracted")

        if log_data["raw_lines"]:
            print(f"  Relevant lines ({len(log_data['raw_lines'])}):")
            for line in log_data["raw_lines"][:5]:
                print(f"    {line}")
            if len(log_data["raw_lines"]) > 5:
                print(f"    ... ({len(log_data['raw_lines']) - 5} more)")
        print()

    print("=" * 60)
    print("Published Validation Reference (HGX-H100):")
    for gpus, data in PUBLISHED_VALIDATION["hgx-h100"].items():
        print(f"  {gpus} GPUs: {data['geomean_error_pct']}% geomean error")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Parse ASTRA-sim simulation results"
    )
    parser.add_argument(
        "results_dir",
        help="Path to directory containing .log files from ASTRA-sim runs",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of human-readable format",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.results_dir):
        print(f"Error: {args.results_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    summary = summarize_results(args.results_dir)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_summary(summary)


if __name__ == "__main__":
    main()
