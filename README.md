# Python Code Execution API

A simple API service that executes arbitrary Python code and returns the result of the `main()` function along with any stdout output.

## Features

- Execute Python scripts via REST API
- Capture and return stdout output
- Support for common libraries (pandas, numpy)
- Lightweight Docker container
- Input validation and error handling
- JSON response format

## API Endpoints

### POST /execute

Executes a Python script and returns the result.

**Request Body:**
```json
{
  "script": "def main():\n    return 'Hello World'"
}
```

**Response (Success):**
```json
{
  "result": "Hello World",
  "stdout": ""
}
```

**Response (Error):**
```json
{
  "error": "Script execution failed",
  "stderr": "Error details...",
  "stdout": "Any output before error"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Usage Examples

### Example 1: Simple function
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    return {\"message\": \"Hello World\", \"number\": 42}"
  }'
```

### Example 2: With stdout output
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    print(\"Processing...\")\n    return \"Done\""
  }'
```

### Example 3: Using pandas
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{
    "script": "import pandas as pd\ndef main():\n    df = pd.DataFrame({\"a\": [1,2,3]})\n    return df.to_dict()"
  }'
```

## Local Development

### Run with Python
```bash
pip install -r requirements.txt
python app.py
```

### Run with Docker
```bash
# Build the image
docker build -t python-executor .

# Run the container
docker run -p 8080:8080 python-executor
```

## Requirements

- Python script must define a `main()` function
- The `main()` function's return value should be JSON-serializable
- Print statements will be captured in the `stdout` field
- Errors will be returned in the `stderr` field

## Security Notes

- This service executes arbitrary code and should only be used in trusted environments
- Consider implementing additional security measures for production use
- The service runs on port 8080 by default

## Deployment

The service is designed to be deployed on Google Cloud Run or similar container platforms. The Docker image exposes port 8080 and is ready for deployment.