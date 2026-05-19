#!/bin/bash

MODEL_URL=https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q8_0.gguf
rm -rf llama/models
mkdir llama/models
curl -L ${MODEL_URL} -o llama/models/model.gguf