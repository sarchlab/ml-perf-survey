"""NeuSight adapter: wraps NeuSight ML-based GPU performance predictions.

NeuSight uses graph neural networks to predict DNN execution latency
across different GPU architectures. Since it requires CUDA at import time,
this adapter reads pre-computed prediction results from CI artifacts.
"""
import json
from pathlib import Path

from prototype.adapters.base import ToolAdapter
from prototype.workload import WorkloadSpec
from prototype.result import ResultSet

RESULTS_DIR = Path(__file__).parent.parent.parent / "data" / "evaluation" / "neusight-results"

# Map WorkloadSpec device names to NeuSight device directory names
DEVICE_MAP = {
    "A100": "NVIDIA_A100-PCIE-40GB",
    "A100-SXM": "NVIDIA_A100-SXM4-40GB",
    "A100-80G": "NVIDIA_A100_80GB_PCIe",
    "H100": "NVIDIA_H100_80GB_HBM3",
    "V100": "Tesla_V100-PCIE-32GB",
    "T4": "Tesla_T4",
    "L4": "NVIDIA_L4",
    "P100": "Tesla_P100-PCIE-16GB",
}

# Map WorkloadSpec model names to NeuSight config prefixes
MODEL_MAP = {
    "ResNet-50": "resnet50",
    "BERT-base": "bert_base",
    "BERT-large": "bert_large",
    "GPT-2": "gpt2_large",
    "VGG-16": "vgg16",
    "InceptionV3": "inceptionv3",
}


class NeuSightAdapter(ToolAdapter):
    """Adapter for NeuSight ML-based GPU latency predictor."""

    @property
    def name(self) -> str:
        return "neusight"

    @property
    def category(self) -> str:
        return "ml-based"

    @property
    def supported_metrics(self) -> list:
        return ["latency_ms", "predicted_latency_ms", "ape_pct"]

    @property
    def supported_workloads(self) -> list:
        return ["cnn", "transformer"]

    def supports(self, spec: WorkloadSpec) -> bool:
        device = spec.hardware.get("device", "")
        model_name = spec.model.get("name", "")
        return device in DEVICE_MAP and model_name in MODEL_MAP

    def run(self, spec: WorkloadSpec) -> ResultSet:
        """Read NeuSight predictions from pre-computed CI results."""
        device = spec.hardware.get("device", "")
        model_name = spec.model.get("name", "")
        mode = "train" if spec.task == "training" else "inf"

        results_file = RESULTS_DIR / "neusight_results.json"
        if not results_file.exists():
            return ResultSet(
                tool=self.name,
                workload=spec.name,
                error="NeuSight results not found. Run NeuSight CI workflow first.",
                exit_code=1,
            )

        with open(results_file) as f:
            data = json.load(f)

        device_short = self._get_device_short(device)
        model_prefix = MODEL_MAP.get(model_name, "")

        # Search per_device_summary for matching results
        best_match = None
        for key, summary in data.get("per_device_summary", {}).items():
            if device_short not in summary.get("device", ""):
                continue
            if summary.get("mode", "") != mode:
                continue

            # Look for model match in per_model results
            for model_result in summary.get("per_model", []):
                config = model_result.get("config", "")
                if model_prefix and model_prefix in config:
                    if best_match is None or model_result.get("ape_pct", 100) < best_match.get("ape_pct", 100):
                        best_match = model_result

        if best_match is None:
            # Return device-level summary if no specific model match
            return self._device_summary(data, device, device_short, mode, spec)

        return ResultSet(
            tool=self.name,
            workload=spec.name,
            metrics={
                "latency_ms": best_match.get("actual_ms", 0),
                "predicted_latency_ms": best_match.get("predicted_ms", 0),
                "ape_pct": best_match.get("ape_pct", 0),
                "config": best_match.get("config", ""),
                "device": best_match.get("device_full", device),
                "source": "precomputed_ci",
            },
        )

    def _get_device_short(self, device):
        """Convert device name to NeuSight short name."""
        mapping = {
            "A100": "A100_40G_PCIe",
            "A100-SXM": "A100_SXM4",
            "A100-80G": "A100_80G_PCIe",
            "H100": "H100",
            "V100": "V100",
            "T4": "T4",
            "L4": "L4",
        }
        return mapping.get(device, device)

    def _device_summary(self, data, device, device_short, mode, spec):
        """Return aggregate device-level accuracy."""
        key = f"{device_short}_{mode}"
        summary = data.get("per_device_summary", {}).get(key)
        if summary:
            return ResultSet(
                tool=self.name,
                workload=spec.name,
                metrics={
                    "mean_ape_pct": summary.get("mean_ape_pct", 0),
                    "num_models": summary.get("num_models", 0),
                    "device": device,
                    "mode": mode,
                    "source": "precomputed_ci_aggregate",
                },
            )

        return ResultSet(
            tool=self.name,
            workload=spec.name,
            error=f"No NeuSight results for device={device} mode={mode}",
            exit_code=1,
        )
