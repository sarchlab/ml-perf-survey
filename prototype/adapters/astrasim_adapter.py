"""ASTRA-sim adapter: wraps ASTRA-sim distributed training simulation results.

ASTRA-sim simulates distributed training communication patterns (all-reduce,
all-gather, etc.) on network topologies like NVSwitch/NVLink.

Since ASTRA-sim requires Docker to build and run, this adapter reads
pre-computed results from CI runs stored in data/evaluation/astra-sim-results/.
For live runs, it delegates to the Docker-based scripts.
"""
import json
import subprocess
from pathlib import Path

from prototype.adapters.base import ToolAdapter
from prototype.workload import WorkloadSpec
from prototype.result import ResultSet

# Pre-computed results directory (populated by CI)
RESULTS_DIR = Path(__file__).parent.parent.parent / "data" / "evaluation" / "astra-sim-results"


class AstraSimAdapter(ToolAdapter):
    """Adapter for ASTRA-sim distributed training simulator."""

    @property
    def name(self) -> str:
        return "astra-sim"

    @property
    def category(self) -> str:
        return "simulation"

    @property
    def supported_metrics(self) -> list:
        return ["total_cycles", "communication_cycles", "compute_cycles", "gpu_count"]

    @property
    def supported_workloads(self) -> list:
        return ["cnn", "transformer", "llm"]

    def supports(self, spec: WorkloadSpec) -> bool:
        return (
            spec.task == "training"
            and spec.hardware.get("count", 1) > 1
            and spec.model_type in self.supported_workloads
        )

    def run(self, spec: WorkloadSpec) -> ResultSet:
        """Run ASTRA-sim or read pre-computed results.

        Tries pre-computed CI results first. Falls back to Docker execution
        if available.
        """
        gpu_count = spec.hardware.get("count", 8)
        model_name = spec.model.get("name", "").lower().replace("-", "")

        # Try pre-computed results
        result = self._read_precomputed(spec, model_name, gpu_count)
        if result is not None:
            return result

        # Try Docker execution
        return self._run_docker(spec, gpu_count)

    def _read_precomputed(self, spec, model_name, gpu_count):
        """Read pre-computed results from CI artifacts."""
        results_file = RESULTS_DIR / "astra_sim_results.json"
        if not results_file.exists():
            return None

        with open(results_file) as f:
            data = json.load(f)

        # Find matching log file
        target_pattern = f"{model_name}_{gpu_count}"
        target_pattern_alt = f"{model_name}_hgx_h100_{gpu_count}gpu_{gpu_count}npus"
        target_pattern_val = f"{model_name}_hgx-h100-validated_{gpu_count}npus"

        for log_entry in data.get("log_files", []):
            fname = log_entry["file"]
            if not log_entry.get("npu_results"):
                continue

            matches = (
                target_pattern in fname
                or target_pattern_alt in fname
                or target_pattern_val in fname
            )
            if not matches:
                continue

            npu_results = log_entry["npu_results"]
            cycles = [r["total_cycles"] for r in npu_results]
            max_cycles = max(cycles)

            # Parse comm/compute from raw lines if available
            comm_cycles = 0
            compute_cycles = 0
            for line in log_entry.get("raw_lines", []):
                if "Comm time:" in line:
                    try:
                        comm_cycles = int(line.split("Comm time:")[-1].strip())
                    except ValueError:
                        pass
                elif "GPU time:" in line:
                    try:
                        compute_cycles = int(line.split("GPU time:")[-1].strip())
                    except ValueError:
                        pass

            return ResultSet(
                tool=self.name,
                workload=spec.name,
                metrics={
                    "total_cycles": max_cycles,
                    "communication_cycles": comm_cycles,
                    "compute_cycles": compute_cycles,
                    "gpu_count": gpu_count,
                    "npus_in_result": len(npu_results),
                    "source": "precomputed_ci",
                },
            )

        return None

    def _run_docker(self, spec, gpu_count):
        """Fall back to Docker-based execution."""
        script_dir = (
            Path(__file__).parent.parent.parent
            / "scripts" / "benchmarks" / "astra-sim"
        )
        if not script_dir.exists():
            return ResultSet(
                tool=self.name,
                workload=spec.name,
                error="ASTRA-sim scripts not found and no pre-computed results available",
                exit_code=1,
            )

        return ResultSet(
            tool=self.name,
            workload=spec.name,
            error=(
                "Live Docker execution not yet supported in adapter. "
                "Run the ASTRA-sim CI workflow to generate results, "
                "then re-run this adapter to read them."
            ),
            exit_code=1,
        )
