"""VIDUR adapter: wraps VIDUR LLM inference serving simulation results.

VIDUR simulates LLM serving systems with different schedulers (vLLM, Sarathi,
Orca) and predicts request-level latency, throughput, and scheduling metrics.

This adapter reads pre-computed results from the VIDUR benchmark data stored
in scripts/benchmarks/vidur/data/results/vidur/. Each subdirectory contains
a config.json and request_metrics.csv from a single scheduler run.
"""
import csv
import json
from pathlib import Path

from prototype.adapters.base import ToolAdapter
from prototype.workload import WorkloadSpec
from prototype.result import ResultSet

# Pre-computed results directory
RESULTS_DIR = (
    Path(__file__).parent.parent.parent
    / "scripts" / "benchmarks" / "vidur" / "data" / "results" / "vidur"
)


class VidurAdapter(ToolAdapter):
    """Adapter for VIDUR LLM inference serving simulator."""

    @property
    def name(self) -> str:
        return "vidur"

    @property
    def category(self) -> str:
        return "simulation"

    @property
    def supported_metrics(self) -> list:
        return [
            "avg_e2e_time_s", "p50_e2e_time_s", "p99_e2e_time_s",
            "avg_ttft_s", "avg_tpot_s", "throughput_tokens_per_s",
        ]

    @property
    def supported_workloads(self) -> list:
        return ["llm"]

    def supports(self, spec: WorkloadSpec) -> bool:
        return (
            spec.model_type == "llm"
            and spec.task in ("inference", "serving")
        )

    def run(self, spec: WorkloadSpec) -> ResultSet:
        """Read pre-computed VIDUR results matching the workload spec."""
        model_name = spec.model.get("name", "").lower()
        device = spec.hardware.get("device", "").lower()
        scheduler = spec.extra.get("scheduler", None)

        if not RESULTS_DIR.exists():
            return ResultSet(
                tool=self.name,
                workload=spec.name,
                error="VIDUR results directory not found.",
                exit_code=1,
            )

        # Scan all result directories for matching configs
        matches = []
        for run_dir in sorted(RESULTS_DIR.iterdir()):
            if not run_dir.is_dir():
                continue
            config_path = run_dir / "config.json"
            csv_path = run_dir / "request_metrics.csv"
            if not config_path.exists() or not csv_path.exists():
                continue

            with open(config_path) as f:
                config = json.load(f)

            cfg_model = config.get("cluster_config", {}).get(
                "replica_config", {}
            ).get("model_name", "")
            cfg_device = config.get("cluster_config", {}).get(
                "replica_config", {}
            ).get("device", "")
            cfg_scheduler = config.get("cluster_config", {}).get(
                "replica_scheduler_config", {}
            ).get("name", "")

            # Match model (fuzzy: check if workload model name appears in config model)
            if not self._model_matches(model_name, cfg_model):
                continue
            # Match device
            if device and device not in cfg_device.lower():
                continue
            # Match scheduler if specified
            if scheduler and scheduler.lower() != cfg_scheduler.lower():
                continue

            metrics = self._parse_csv(csv_path, cfg_scheduler)
            if metrics is not None:
                matches.append((cfg_scheduler, metrics))

        if not matches:
            return ResultSet(
                tool=self.name,
                workload=spec.name,
                error=f"No VIDUR results for model={model_name} device={device}",
                exit_code=1,
            )

        # If scheduler was specified, return that single result
        if scheduler and len(matches) == 1:
            sched_name, metrics = matches[0]
            metrics["scheduler"] = sched_name
            metrics["source"] = "precomputed"
            return ResultSet(
                tool=self.name,
                workload=spec.name,
                metrics=metrics,
            )

        # Otherwise return the best scheduler (lowest avg E2E) and note others
        matches.sort(key=lambda m: m[1].get("avg_e2e_time_s", float("inf")))
        best_sched, best_metrics = matches[0]
        best_metrics["scheduler"] = best_sched
        best_metrics["source"] = "precomputed"
        best_metrics["schedulers_available"] = [m[0] for m in matches]
        return ResultSet(
            tool=self.name,
            workload=spec.name,
            metrics=best_metrics,
        )

    def _model_matches(self, workload_model, config_model):
        """Check if workload model name matches the VIDUR config model."""
        workload_model = workload_model.lower().replace("-", "").replace("_", "")
        config_model = config_model.lower().replace("-", "").replace("_", "")
        # Handle common cases: "llama-2-7b" matches "meta-llama/Llama-2-7b-hf"
        if workload_model in config_model:
            return True
        # Try just the model family name
        for token in workload_model.split("/"):
            if token and token in config_model:
                return True
        return False

    def _parse_csv(self, csv_path, scheduler_name):
        """Parse VIDUR request_metrics.csv into summary metrics."""
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            return None

        e2e_times = [float(r["request_e2e_time"]) for r in rows]
        exec_times = [float(r["request_execution_time"]) for r in rows]
        sched_delays = [float(r["request_scheduling_delay"]) for r in rows]
        prefill_times = [float(r["prefill_e2e_time"]) for r in rows]
        num_tokens = [int(r["request_num_tokens"]) for r in rows]
        num_prefill = [int(r["request_num_prefill_tokens"]) for r in rows]
        num_decode = [int(r["request_num_decode_tokens"]) for r in rows]

        e2e_sorted = sorted(e2e_times)
        n = len(e2e_sorted)

        # TPOT: decode time / decode tokens per request
        tpot_values = []
        for r in rows:
            dec = int(r["request_num_decode_tokens"])
            if dec > 0:
                decode_time = float(r["request_e2e_time"]) - float(r["prefill_e2e_time"])
                tpot_values.append(decode_time / dec)

        return {
            "avg_e2e_time_s": sum(e2e_times) / n,
            "p50_e2e_time_s": e2e_sorted[n // 2],
            "p99_e2e_time_s": e2e_sorted[int(n * 0.99)],
            "avg_ttft_s": sum(prefill_times) / n,
            "avg_tpot_s": sum(tpot_values) / len(tpot_values) if tpot_values else 0,
            "throughput_tokens_per_s": sum(num_tokens) / max(e2e_times),
            "avg_exec_time_s": sum(exec_times) / n,
            "avg_sched_delay_s": sum(sched_delays) / n,
            "num_requests": n,
            "avg_prefill_tokens": sum(num_prefill) / n,
            "avg_decode_tokens": sum(num_decode) / n,
        }
