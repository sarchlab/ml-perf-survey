#!/usr/bin/env python3
"""mlperf-model: Unified CLI for ML performance modeling tools.

This is the entry point for the unified tool prototype (Contribution 3).
It wraps multiple ML performance prediction/simulation tools behind a
common interface with standardized workload specs and result formats.

Usage:
    python -m prototype.cli list
    python -m prototype.cli run --workload configs/resnet50.yaml --tool vidur
    python -m prototype.cli compare --workload configs/resnet50.yaml --tools vidur,astra-sim
"""
import argparse
import json
import sys
from pathlib import Path

from prototype.workload import WorkloadSpec
from prototype.result import ResultSet
from prototype.adapters import get_adapter, list_adapters


def cmd_list(args):
    """List available tools and their capabilities."""
    adapters = list_adapters()
    print(f"Available tools ({len(adapters)}):")
    print()
    for name, adapter_cls in adapters.items():
        a = adapter_cls()
        print(f"  {name}")
        print(f"    Category:   {a.category}")
        print(f"    Metrics:    {', '.join(a.supported_metrics)}")
        print(f"    Workloads:  {', '.join(a.supported_workloads)}")
        print()


def cmd_run(args):
    """Run a prediction/simulation with the specified tool."""
    # Load workload spec
    spec = WorkloadSpec.from_yaml(args.workload)
    print(f"Workload: {spec.name} ({spec.model_type})")
    print(f"Tool:     {args.tool}")
    print()

    # Get adapter
    adapter_cls = get_adapter(args.tool)
    if adapter_cls is None:
        print(f"Error: Unknown tool '{args.tool}'. Use 'list' to see available tools.")
        sys.exit(1)

    adapter = adapter_cls()
    if not adapter.supports(spec):
        print(f"Error: {args.tool} does not support workload '{spec.name}'")
        sys.exit(1)

    # Run
    print(f"Running {args.tool}...")
    result = adapter.run(spec)

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"Results saved to {output_path}")
    else:
        print()
        result.print_summary()


def cmd_compare(args):
    """Run a workload across multiple tools and compare results."""
    spec = WorkloadSpec.from_yaml(args.workload)
    tool_names = [t.strip() for t in args.tools.split(",")]

    print(f"Workload: {spec.name} ({spec.model_type})")
    print(f"Tools:    {', '.join(tool_names)}")
    print()

    results = []
    for tool_name in tool_names:
        adapter_cls = get_adapter(tool_name)
        if adapter_cls is None:
            print(f"  SKIP {tool_name}: not found")
            continue
        adapter = adapter_cls()
        if not adapter.supports(spec):
            print(f"  SKIP {tool_name}: does not support this workload")
            continue
        print(f"  Running {tool_name}...")
        result = adapter.run(spec)
        results.append(result)

    if not results:
        print("No tools produced results.")
        sys.exit(1)

    # Print comparison table
    print()
    ResultSet.print_comparison(results)


def cmd_validate(args):
    """Run all compatible tools on each workload config and report results."""
    configs_dir = Path(args.configs) if args.configs else Path(__file__).parent / "configs"
    if not configs_dir.exists():
        print(f"Error: configs directory '{configs_dir}' not found.")
        sys.exit(1)

    yaml_files = sorted(configs_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"No workload configs found in {configs_dir}")
        sys.exit(1)

    adapters = list_adapters()
    all_results = []
    errors = []

    print(f"Validating {len(yaml_files)} workload(s) against {len(adapters)} tool(s)")
    print("=" * 70)

    for yaml_file in yaml_files:
        spec = WorkloadSpec.from_yaml(str(yaml_file))
        print(f"\n--- {spec.name} ({spec.model_type}, {spec.task}) ---")

        for name, adapter_cls in adapters.items():
            adapter = adapter_cls()
            if not adapter.supports(spec):
                continue
            result = adapter.run(spec)
            all_results.append(result)
            status = "OK" if result.exit_code == 0 else "FAIL"
            if result.error:
                errors.append(f"{spec.name}/{name}: {result.error}")
                print(f"  {name:<15} {status}  (error: {result.error})")
            else:
                metric_summary = ", ".join(
                    f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
                    for k, v in list(result.metrics.items())[:3]
                )
                print(f"  {name:<15} {status}  {metric_summary}")

    # Summary
    ok_count = sum(1 for r in all_results if r.exit_code == 0)
    fail_count = sum(1 for r in all_results if r.exit_code != 0)
    print(f"\n{'=' * 70}")
    print(f"Total: {ok_count} passed, {fail_count} failed, "
          f"{len(all_results)} total runs across {len(yaml_files)} workloads")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "workloads": len(yaml_files),
            "tools": len(adapters),
            "total_runs": len(all_results),
            "passed": ok_count,
            "failed": fail_count,
            "results": [r.to_dict() for r in all_results],
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nFull report saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        prog="mlperf-model",
        description="Unified CLI for ML performance modeling tools",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List available tools")

    # run
    run_parser = subparsers.add_parser("run", help="Run a tool on a workload")
    run_parser.add_argument("--workload", "-w", required=True, help="Path to workload YAML")
    run_parser.add_argument("--tool", "-t", required=True, help="Tool name")
    run_parser.add_argument("--output", "-o", help="Output JSON file path")

    # compare
    cmp_parser = subparsers.add_parser("compare", help="Compare tools on a workload")
    cmp_parser.add_argument("--workload", "-w", required=True, help="Path to workload YAML")
    cmp_parser.add_argument("--tools", "-t", required=True, help="Comma-separated tool names")

    # validate
    val_parser = subparsers.add_parser("validate", help="Run all tools on all workloads")
    val_parser.add_argument("--configs", "-c", help="Configs directory (default: prototype/configs)")
    val_parser.add_argument("--output", "-o", help="Output JSON report path")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "validate":
        cmd_validate(args)


if __name__ == "__main__":
    main()
