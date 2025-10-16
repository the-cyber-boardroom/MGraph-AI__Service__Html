# MGraph-AI__Service__Html

**Version:** v0.1.0  
**Purpose:** Pure HTML structural transformation service

## Overview

MGraph-AI__Service__Html is a specialized service for HTML structure manipulation. It provides fast, deterministic HTML processing operations without any LLM dependencies. This service is part of the MGraph-AI ecosystem and focuses exclusively on HTML structural transformations.

## Key Features

- ✅ **No LLM Dependencies** - Pure HTML processing only
- ✅ **Type-Safe** - All operations use Type_Safe classes
- ✅ **Serverless Ready** - Optimized for AWS Lambda deployment
- ✅ **Atomic & Compound Operations** - Flexible API design
- ✅ **Round-Trip Validation** - Quality assurance built-in
- ✅ **Hash-Based Text Node Extraction** - Stable content addressing

## Architecture

### Separation of Concerns

```
┌───────────────────────────────────────────────┐
│              Mitmproxy                        │
│           (HTML Interception)                 │
└───────────────┬───────────────────────────────┘
                │ Raw HTML
                ▼
┌───────────────────────────────────────────────┐
│      MGraph-AI__Service__Html                 │ ← THIS SERVICE
│                                               │
│  • HTML ↔ html_dict conversion                │
│  • Text node extraction with stable hashes    │
│  • HTML reconstruction from hash mappings     │
│  • Visual transformations (hashes, xxx masks) │
│  • Structure validation (round-trip testing)  │
└───────────────┬───────────────────────────────┘
                │ {hash: text} mappings
                ▼
┌───────────────────────────────────────────────┐
│   MGraph-AI__Service__Semantic_Text           │ ← SEPARATE SERVICE
│                                               │
│  • Text → LLM ratings                         │
│  • Sentiment analysis                         │
│  • Topic extraction                           │
└───────────────────────────────────────────────┘
```

## API Endpoints

### HTML Routes (`/html/*`)

#### Atomic Operations
- `POST /html/to/dict` - Parse HTML string into html_dict structure
- `POST /html/to/html` - Round-trip validation (HTML → dict → HTML)

#### Compound Operations
- `POST /html/to/text/nodes` - HTML → dict → text_nodes in one call
- `POST /html/to/lines` - HTML → dict → formatted line representation
- `POST /html/to/html/hashes` - Replace all text with hashes (visual debug)
- `POST /html/to/html/xxx` - Replace all text with 'x' characters (privacy mask)

### Dict Routes (`/dict/*`)
- `POST /dict/to/html` - Reconstruct HTML from html_dict
- `POST /dict/to/text/nodes` - Extract text nodes from html_dict
- `POST /dict/to/lines` - Format html_dict as readable lines

### Hash Routes (`/hashes/*`)
- `POST /hashes/to/html` - Reconstruct HTML with custom text replacements

## Installation

```bash
pip install mgraph-ai-service-html
```

## Quick Start

### Python Client Example

```python
import requests

# Parse HTML to dict
response = requests.post(
    "https://html.mgraph.ai/html/to/dict",
    json={"html": "<html><body>Hello World</body></html>"}
)
html_dict = response.json()["html_dict"]

# Extract text nodes
response = requests.post(
    "https://html.mgraph.ai/html/to/text/nodes",
    json={"html": "<html><body>Hello World</body></html>"}
)
text_nodes = response.json()["text_nodes"]
```

## Development

### Project Structure

```
mgraph_ai_service_html/
├── html__fast_api/
│   ├── Html__Fast_API.py        # Main FastAPI app
│   ├── core/                    # Core transformation logic
│   ├── routes/                  # API route handlers
│   └── schemas/                 # Type_Safe request/response schemas
├── lambdas/
│   └── lambda_handler.py        # AWS Lambda entry point
└── utils/
    └── Version.py               # Version management
```

### Running Locally

```python
from mgraph_ai_service_html.html__fast_api.Html__Fast_API import Html__Fast_API

with Html__Fast_API() as api:
    api.setup()
    app = api.app()
    # Use with uvicorn: uvicorn main:app --reload
```

## Key Design Principles

1. **No Business Logic in Schemas** - Schemas are pure data structures
2. **Atomic Operations** - Maximum caching control for callers
3. **No Built-in Caching** - Caller's responsibility
4. **Type_Safe Throughout** - Runtime type checking on all operations
5. **No LLM Dependencies** - Fast, deterministic operations only

## License

MIT License - See LICENSE file for details

## Related Services

- **MGraph-AI__Service__Cache** - Caching layer for HTML operations
- **MGraph-AI__Service__Semantic_Text** - LLM-based text analysis
- **MGraph-AI__Service__LLMs** - LLM provider abstraction

## Version History

- **v0.1.0** (2025-10-15) - Initial release
  - Pure HTML structural transformation
  - Atomic and compound operations
  - Type_Safe throughout
  - AWS Lambda ready
