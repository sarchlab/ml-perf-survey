"""Tool adapters for the unified ML performance modeling prototype."""
from prototype.adapters.base import ToolAdapter
from prototype.adapters.timeloop_adapter import TimeloopAdapter
from prototype.adapters.analytical_adapter import AnalyticalAdapter
from prototype.adapters.astrasim_adapter import AstraSimAdapter
from prototype.adapters.neusight_adapter import NeuSightAdapter

_ADAPTERS = {
    "timeloop": TimeloopAdapter,
    "analytical": AnalyticalAdapter,
    "astra-sim": AstraSimAdapter,
    "neusight": NeuSightAdapter,
}


def get_adapter(name: str):
    """Get an adapter class by name."""
    return _ADAPTERS.get(name.lower())


def list_adapters():
    """Return all registered adapters."""
    return dict(_ADAPTERS)
