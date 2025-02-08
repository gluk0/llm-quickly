import pytest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment variables
os.environ['BUCKET_NAME'] = 'test-bucket'
os.environ['MODEL_FOLDER'] = 'test-model'
os.environ['LOCAL_PATH'] = '/tmp/test-model' 