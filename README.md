# llm-quickly

A FastAPI service for quick and efficient LLM inference using Google Cloud Storage for model management,
reducing container build times and deployment times significantly. 

## 🚀 Features

- Fast model serving with PyTorch and Transformers
- Google Cloud Storage integration for model storage
- GPU acceleration support
- Configurable inference parameters
- Production-ready with Docker support
- Simple load testing utilities included

## 📋 Prerequisites

- Python 3.8+
- Google Cloud Platform account with Storage access
- CUDA-compatible GPU (optional, for GPU acceleration). 
- Docker (for containerized deployment)

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/rich-clarke/llm-quickly.git
cd llm-quickly
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
```

4. Build and run the service:

```bash
docker build -t llm-quickly .
docker run -d -p 8000:8000 llm-quickly
```

5. Test the service:

```bash
python -m utility.load_test
```

## ⚙️ Configuration

The following environment variables need to be configured:

- `BUCKET_NAME`: Your Google Cloud Storage bucket name
- `MODEL_FOLDER`: Path to your model in GCS
- `LOCAL_PATH`: Local path to store downloaded model files
