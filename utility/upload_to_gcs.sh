#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}llm-quickly: $1${NC}"
}

log_error() {
    echo -e "${RED}llm-quickly: $1${NC}"
}

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

log_info "Starting model download script..."
cd "${PROJECT_ROOT}"

log_info "Setting up poetry..."
poetry install 

export BUCKET_NAME="rich-clarke-dev-models"

MODEL_FOLDERS=$(find "${PROJECT_ROOT}/models/local" -mindepth 1 -maxdepth 1 -type d)

if [ -z "$MODEL_FOLDERS" ]; then
    log_error "No model folders found in ${PROJECT_ROOT}/models/local"
    exit 1
fi

for MODEL_FOLDER in $MODEL_FOLDERS; do
    MODEL_NAME=$(basename "$MODEL_FOLDER")
    LOCAL_PATH="models/local/${MODEL_NAME}"
    export MODEL_FOLDER="${LOCAL_PATH}"

    log_info "Processing model: ${MODEL_NAME}"
    
    # # Download model from HuggingFace
    # log_info "Downloading model from HuggingFace..."
    # python -m utility.cli download-model \
    #     --model-name "TinyLlama/TinyLlama-1.1B-Chat-v1.0" \
    #     --path "${LOCAL_PATH}"

    log_info "Uploading model to GCS bucket: ${BUCKET_NAME}" && 
    poetry run python -m utility.setup.model_utils upload-model \
        --local-path "${LOCAL_PATH}" \
        --bucket "${BUCKET_NAME}" \
        --path "${LOCAL_PATH}" 

        
    log_info "Model download and upload complete!"
    log_info "You can now use this model with the following environment variables:"
    echo -e "BUCKET_NAME=${BUCKET_NAME}"
    echo -e "MODEL_FOLDER=${MODEL_FOLDER}"
    echo -e "LOCAL_PATH=${LOCAL_PATH}"
    log_info "Model processing completed successfully!"
done

exit 0 