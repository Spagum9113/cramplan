#!/bin/bash

export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)
echo "Exported OPENAI_API_KEY" 