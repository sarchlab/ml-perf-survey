#!/usr/bin/env python3
"""Analyze VIDUR simulation results across schedulers.

Usage:
    python3 scripts/benchmarks/vidur/analyze_results.py <results_dir>
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path


def analyze_scheduler_run(run_dir):
    """Analyze a single VIDUR scheduler run."""
    metrics = {"run_dir": str(run_dir)}

    # Read config
    config_path = run_dir / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        metrics["model"] = config.get("replica_config", {}).get("model_name", "unknown")
        metrics["device"] = config.get("replica_config", {}).get("device", "unknown")
        metrics["scheduler"] = config.get("replica_scheduler_config", {}).get("type", "unknown")
        metrics["num_requests"] = config.get("synthetic_request_generator_config", {}).get("num_requests", 0)

    # Read request metrics
    csv_path = run_dir / "request_metrics.csv"
    if not csv_path.exists():
        metrics["error"] = "No request_metrics.csv found"
        return metrics

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        metrics["error"] = "Empty CSV"
        return metrics

    # Compute statistics
    e2e_times = [float(r["request_e2e_time"]) for r in rows]
    exec_times = [float(r["request_execution_time"]) for r in rows]
    sched_delays = [float(r["request_scheduling_delay"]) for r in rows]
    num_tokens = [int(r["request_num_tokens"]) for r in rows]
    prefill_tokens = [int(r["request_num_prefill_tokens"]) for r in rows]
    decode_tokens = [int(r["request_num_decode_tokens"]) for r in rows]

    metrics["num_completed"] = len(rows)
    metrics["avg_e2e_time_s"] = sum(e2e_times) / len(e2e_times)
    metrics["avg_exec_time_s"] = sum(exec_times) / len(exec_times)
    metrics["avg_sched_delay_s"] = sum(sched_delays) / len(sched_delays)
    metrics["p50_e2e_time_s"] = sorted(e2e_times)[len(e2e_times) // 2]
    metrics["p99_e2e_time_s"] = sorted(e2e_times)[int(len(e2e_times) * 0.99)]
    metrics["avg_tokens"] = sum(num_tokens) / len(num_tokens)
    metrics["avg_prefill_tokens"] = sum(prefill_tokens) / len(prefill_tokens)
    metrics["avg_decode_tokens"] = sum(decode_tokens) / len(decode_tokens)
    metrics["total_tokens"] = sum(num_tokens)
    metrics["throughput_tokens_per_s"] = sum(num_tokens) / max(e2e_times)

    return metrics


def main():
    parser = argparse.ArgumentParser(description="Analyze VIDUR results")
    parser.add_argument("results_dir", help="Directory containing scheduler subdirectories")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    all_results = []

    for scheduler_dir in sorted(results_dir.iterdir()):
        if not scheduler_dir.is_dir():
            continue
        # Find the timestamped run directory
        for run_dir in sorted(scheduler_dir.iterdir()):
            if run_dir.is_dir() and (run_dir / "config.json").exists():
                result = analyze_scheduler_run(run_dir)
                all_results.append(result)

    if args.json:
        print(json.dumps(all_results, indent=2))
    else:
        print("=" * 70)
        print("VIDUR Results Summary")
        print("=" * 70)
        for r in all_results:
            sched = r.get("scheduler", "unknown")
            print(f"\n--- {sched} ---")
            if "error" in r:
                print(f"  Error: {r['error']}")
                continue
            print(f"  Model: {r.get('model', 'N/A')}")
            print(f"  Device: {r.get('device', 'N/A')}")
            print(f"  Requests: {r.get('num_completed', 0)}")
            print(f"  Avg E2E time: {r.get('avg_e2e_time_s', 0):.4f}s")
            print(f"  Avg Execution time: {r.get('avg_exec_time_s', 0):.4f}s")
            print(f"  Avg Scheduling delay: {r.get('avg_sched_delay_s', 0):.6f}s")
            print(f"  P50 E2E time: {r.get('p50_e2e_time_s', 0):.4f}s")
            print(f"  P99 E2E time: {r.get('p99_e2e_time_s', 0):.4f}s")
            print(f"  Avg tokens/request: {r.get('avg_tokens', 0):.0f}")
            print(f"  Throughput: {r.get('throughput_tokens_per_s', 0):.0f} tokens/s")
        print()


if __name__ == "__main__":
    main()
