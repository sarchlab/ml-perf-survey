#!/usr/bin/env python3
"""Convert ASTRA-sim v1.0 text workload to Chakra ET traces for v2.0.

Fixes the import issue by using direct sys.path manipulation instead of
relying on the chakra package being installed.

Usage:
    python3 gen_traces.py --input <workload.txt> --output <prefix> --num-npus 8
"""
import argparse
import os
import sys

# Fix import path for Chakra protobuf definitions
CHAKRA_PATHS = [
    "/app/astra-sim/extern/graph_frontend",
]
for p in CHAKRA_PATHS:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from chakra.schema.protobuf.et_def_pb2 import (
    ALL_REDUCE,
    COMM_COLL_NODE,
    COMP_NODE,
    GlobalMetadata,
    Node,
)
from google.protobuf.internal.encoder import _EncodeVarint


def parse_v1_workload(filepath):
    """Parse ASTRA-sim v1.0 tab-delimited workload file."""
    layers = []
    with open(filepath) as f:
        lines = [l.strip() for l in f if l.strip()]

    strategy = lines[0]
    num_layers = int(lines[1])

    for i in range(2, 2 + num_layers):
        parts = lines[i].split("\t")
        if len(parts) < 12:
            parts = lines[i].split()
        if len(parts) < 12:
            print(f"WARNING: Skipping malformed line {i}: {lines[i][:80]}")
            continue

        layers.append({
            "name": parts[0],
            "fwd_compute": int(parts[2]),
            "inp_grad": int(parts[5]),
            "wt_grad": int(parts[8]),
            "collective": parts[9],
            "comm_size": int(parts[10]),
            "delay": int(parts[11]),
        })

    return layers, strategy


def generate_et(layers, output_prefix, num_npus):
    """Generate Chakra ET protobuf traces."""
    for npu_id in range(num_npus):
        output_file = f"{output_prefix}.{npu_id}.et"
        with open(output_file, "wb") as f:
            meta = GlobalMetadata()
            meta.version = "0.0.4"
            meta_bytes = meta.SerializeToString()
            _EncodeVarint(f.write, len(meta_bytes))
            f.write(meta_bytes)

            node_id = 0
            prev_id = None

            for layer in layers:
                # Forward compute node
                fwd = Node()
                fwd.id = node_id
                fwd.name = layer["name"] + "_fwd"
                fwd.type = COMP_NODE
                fwd.duration_micros = layer["fwd_compute"]
                if prev_id is not None:
                    fwd.data_deps.append(prev_id)
                prev_id = node_id
                node_id += 1
                fwd_bytes = fwd.SerializeToString()
                _EncodeVarint(f.write, len(fwd_bytes))
                f.write(fwd_bytes)

                # Backward input gradient
                bwd_i = Node()
                bwd_i.id = node_id
                bwd_i.name = layer["name"] + "_bwd_inp"
                bwd_i.type = COMP_NODE
                bwd_i.duration_micros = layer["inp_grad"]
                bwd_i.data_deps.append(prev_id)
                prev_id = node_id
                node_id += 1
                bwd_i_bytes = bwd_i.SerializeToString()
                _EncodeVarint(f.write, len(bwd_i_bytes))
                f.write(bwd_i_bytes)

                # Backward weight gradient
                bwd_w = Node()
                bwd_w.id = node_id
                bwd_w.name = layer["name"] + "_bwd_wt"
                bwd_w.type = COMP_NODE
                bwd_w.duration_micros = layer["wt_grad"]
                bwd_w.data_deps.append(prev_id)
                prev_id = node_id
                node_id += 1
                bwd_w_bytes = bwd_w.SerializeToString()
                _EncodeVarint(f.write, len(bwd_w_bytes))
                f.write(bwd_w_bytes)

                # Communication (all-reduce)
                if layer["collective"] == "ALLREDUCE" and layer["comm_size"] > 0:
                    comm = Node()
                    comm.id = node_id
                    comm.name = layer["name"] + "_allreduce"
                    comm.type = COMM_COLL_NODE
                    ca = comm.attr.add()
                    ca.name = "comm_size"
                    ca.int64_val = layer["comm_size"]
                    ct = comm.attr.add()
                    ct.name = "comm_type"
                    ct.int64_val = int(ALL_REDUCE)
                    comm.data_deps.append(prev_id)
                    prev_id = node_id
                    node_id += 1
                    comm_bytes = comm.SerializeToString()
                    _EncodeVarint(f.write, len(comm_bytes))
                    f.write(comm_bytes)

            print(f"  Generated {output_file} ({node_id} nodes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert ASTRA-sim v1.0 text workload to Chakra ET traces"
    )
    parser.add_argument("--input", required=True, help="Path to v1.0 workload txt file")
    parser.add_argument("--output", required=True, help="Output prefix for .et files")
    parser.add_argument("--num-npus", type=int, default=8, help="Number of NPUs")
    args = parser.parse_args()

    layers, strategy = parse_v1_workload(args.input)
    print(f"Parsed {len(layers)} layers, strategy: {strategy}")
    generate_et(layers, args.output, args.num_npus)
    print("Done!")
