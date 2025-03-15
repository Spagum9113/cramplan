# OpenAI API Configuration with Tracing

This directory contains code for using the OpenAI API with proper configuration and tracing.

## Setting Up Your OpenAI API Key

To set up your OpenAI API key:

1. Make the export script executable (first time only):
   ```bash
   chmod +x export_key.sh
   ```

2. Export your API key from the .env file:
   ```bash
   source ./export_key.sh
   ```

3. Now you can run your Python code with the exported API key.

## Quick Start (No External Services Required)