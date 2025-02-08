#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' 

# Get the project root directory (2 levels up from script location)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo -e "${GREEN}Starting model download script...${NC}"
cd "${PROJECT_ROOT}"

# if [ ! -d "venv" ]; then
#     echo -e "${GREEN}Creating virtual environment...${NC}"
#     python3 -m venv venv
# fi

# echo -e "${GREEN}Activating virtual environment...${NC}"
# source venv/bin/activate

# # Check for requirements.txt in project root
# if [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
#     echo -e "${RED}Error: requirements.txt not found in ${PROJECT_ROOT}${NC}"
#     exit 1
# fi

# echo -e "${GREEN}Installing requirements...${NC}"
# pip install -r "${PROJECT_ROOT}/requirements.txt"

# # Create directories if they don't exist
# mkdir -p "${PROJECT_ROOT}/models/local/tinyllama"

# export MODEL_NAME="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# export BUCKET_NAME="rich-clarke-dev-models"
# export MODEL_FOLDER="models/tinyllama"
# export LOCAL_PATH="${PROJECT_ROOT}/models/local/tinyllama"

# echo -e "${GREEN}Downloading model: ${MODEL_NAME}${NC}"
# echo -e "${GREEN}To bucket: ${BUCKET_NAME}/${MODEL_FOLDER}${NC}"

# # First download the model locally using transformers
# echo -e "${GREEN}Downloading model from Hugging Face...${NC}"
# python -c "
# from transformers import AutoModelForCausalLM, AutoTokenizer
# model = AutoModelForCausalLM.from_pretrained('${MODEL_NAME}')
# tokenizer = AutoTokenizer.from_pretrained('${MODEL_NAME}')
# model.save_pretrained('${LOCAL_PATH}')
# tokenizer.save_pretrained('${LOCAL_PATH}')
# "

# Then upload to GCS
echo -e "${GREEN}Uploading model to GCS...${NC}"
python -m utility.cli upload-model \
    --bucket "${BUCKET_NAME}" \
    --path "${LOCAL_PATH}"

echo -e "${GREEN}Model download and upload complete!${NC}"
echo -e "${GREEN}You can now use this model with the following environment variables:${NC}"
echo -e "BUCKET_NAME=${BUCKET_NAME}"
echo -e "MODEL_FOLDER=${MODEL_FOLDER}"
echo -e "LOCAL_PATH=${LOCAL_PATH}"

deactivate

echo -e "${GREEN}Script completed successfully!${NC}" 