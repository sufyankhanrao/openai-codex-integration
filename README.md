# openai-codex-integration

This repository demonstrates a minimal Petstore SDK built with robust
abstractions and a documented API surface. It includes:

- **OpenAPI spec** (`petstore-openapi.yaml`) describing available endpoints
- **Python SDK** under `petstore_sdk/` with configurable transports and hooks
- **Tests** exercising the client behaviour

## Development

Install dependencies and run the test suite:

```bash
pip install -r requirements.txt
pytest -q
```

The SDK is intended as a starting point for further experimentation.
