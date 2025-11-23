#!/bin/bash -e

# This script generates the python protobuf code for kfp.pipeline_spec and kfp.kubernetes.
# It assumes it is run from the sdk/python directory.

REPO_ROOT=$(cd "$(dirname "$0")/../.." && pwd)

# Generate kfp.pipeline_spec
echo "Generating kfp.pipeline_spec..."
python3 -m grpc_tools.protoc -I"$REPO_ROOT/api/v2alpha1" \
    --python_out="$REPO_ROOT/sdk/python/kfp/pipeline_spec" \
    "$REPO_ROOT/api/v2alpha1/pipeline_spec.proto"

# Generate kfp.kubernetes
echo "Generating kfp.kubernetes..."
python3 -m grpc_tools.protoc -I"$REPO_ROOT/kubernetes_platform/proto" -I"$REPO_ROOT/api/v2alpha1" \
    --python_out="$REPO_ROOT/sdk/python/kfp/kubernetes" \
    "$REPO_ROOT/kubernetes_platform/proto/kubernetes_executor_config.proto"

echo "Done."
