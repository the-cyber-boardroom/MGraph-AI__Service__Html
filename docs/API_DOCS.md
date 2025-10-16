# API Documentation - MGraph-AI__Service__Html

**Version:** v0.1.0  
**Base URL:** `https://html.mgraph.ai` (production)

## Overview

The HTML Service provides pure structural transformation operations on HTML content. All endpoints use POST requests with JSON payloads and return JSON responses (except where noted).

## Authentication

Currently, the service is open for testing. Production deployment will require API key authentication via headers.

## Endpoints

### HTML Routes (tag: `html`)

#### `POST /html/to/dict`

Parse HTML string into html_dict structure.

**Request Body:**
```json
{
  "html": "<html><body>Content</body></html>"
}
```

**Response:**
```json
{
  "html_dict": { /* html_dict structure */ },
  "node_count": 15,
  "max_depth": 5
}
```

**Use Case:** Initial parsing step for caching html_dict structure.

---

#### `POST /html/to/html`

Round-trip validation: HTML → dict → HTML.

**Request Body:**
```json
{
  "html": "<html><body>Content</body></html>"
}
```

**Response:** HTML content (text/html)

**Use Case:** Quality assurance - verify transformation fidelity.

---

#### `POST /html/to/text/nodes`

One-shot extraction: HTML → dict → text_nodes.

**Request Body:**
```json
{
  "html": "<html><body><p>Hello</p></body></html>",
  "max_depth": 256
}
```

**Response:**
```json
{
  "text_nodes": {
    "a1b2c3d4e5": {
      "original_text": "Hello",
      "tag": "p"
    }
  },
  "total_nodes": 1,
  "max_depth_reached": false
}
```

**Use Case:** Extract all text content with stable hash identifiers.

---

#### `POST /html/to/lines`

Convert HTML to human-readable line format.

**Request Body:**
```json
{
  "html": "<html><body>Content</body></html>"
}
```

**Response:** Plain text representation (text/plain)

**Use Case:** Debugging, inspection, human review.

---

#### `POST /html/to/html/hashes`

Visual debug: replace all text with hash values.

**Request Body:**
```json
{
  "html": "<html><body><p>Secret</p></body></html>",
  "max_depth": 256
}
```

**Response:** HTML with hashes (text/html)
```html
<html><body><p>a1b2c3d4e5</p></body></html>
```

**Use Case:** Verify hash extraction, debug text identification.

---

#### `POST /html/to/html/xxx`

Privacy mask: replace all text with 'x' characters.

**Request Body:**
```json
{
  "html": "<html><body><p>Secret Text</p></body></html>",
  "max_depth": 256
}
```

**Response:** HTML with xxx (text/html)
```html
<html><body><p>xxxxxx xxxx</p></body></html>
```

**Use Case:** Preserve structure while hiding content.

---

### Dict Routes (tag: `dict`)

#### `POST /dict/to/html`

Reconstruct HTML from html_dict.

**Request Body:**
```json
{
  "html_dict": { /* html_dict structure */ }
}
```

**Response:** HTML content (text/html)

**Use Case:** Final step after modifications - reconstruct HTML.

---

#### `POST /dict/to/text/nodes`

Extract text nodes from cached html_dict.

**Request Body:**
```json
{
  "html_dict": { /* html_dict structure */ },
  "max_depth": 256
}
```

**Response:**
```json
{
  "text_nodes": { /* hash: node_data */ },
  "total_nodes": 5,
  "max_depth_reached": false
}
```

**Use Case:** Work with cached html_dict instead of reparsing HTML.

---

#### `POST /dict/to/lines`

Format html_dict as readable lines.

**Request Body:**
```json
{
  "html_dict": { /* html_dict structure */ }
}
```

**Response:** Plain text representation (text/plain)

**Use Case:** Debug cached html_dict structure.

---

### Hash Routes (tag: `hashes`)

#### `POST /hashes/to/html`

**CRITICAL ENDPOINT:** Reconstruct HTML with custom text replacements. This is how external services (like Semantic_Text) modify HTML content.

**Request Body:**
```json
{
  "html_dict": { /* html_dict structure */ },
  "hash_mapping": {
    "a1b2c3d4e5": "Replacement text 1",
    "f6g7h8i9j0": "Replacement text 2"
  }
}
```

**Response:** Modified HTML (text/html)

**Use Case:** Apply external modifications (ratings, filters, translations).

---

## Typical Workflows

### High-Volume Site (with Caching)

```
1. POST /html/to/dict 
   → Cache html_dict (1 hour TTL)

2. POST /dict/to/text/nodes 
   → Cache text_nodes (indefinite)

3. External Service: Process text_nodes
   → Cache ratings (1 week TTL)

4. POST /hashes/to/html 
   → Generate filtered HTML
```

### Low-Volume Site (Simple)

```
1. POST /html/to/text/nodes
   → Get text_nodes directly

2. External Service: Process text_nodes

3. POST /hashes/to/html
   → Generate filtered HTML
```

### Quality Assurance

```
1. POST /html/to/html
   → Verify round-trip fidelity

2. Compare input vs output
   → Check structural preservation
```

## Error Responses

All endpoints return standard HTTP status codes:

- **200 OK** - Success
- **400 Bad Request** - Invalid request schema
- **422 Unprocessable Entity** - Type validation failed
- **500 Internal Server Error** - Service error

Error response format:
```json
{
  "detail": "Error description"
}
```

## Rate Limits

Current limits (subject to change):
- 100 requests per minute per IP
- 1000 requests per hour per IP

## OpenAPI Documentation

Interactive API documentation available at:
- **Swagger UI:** `https://html.mgraph.ai/docs`
- **ReDoc:** `https://html.mgraph.ai/redoc`

## SDKs & Client Libraries

### Python Client Example

```python
import requests

class HtmlServiceClient:
    def __init__(self, base_url="https://html.mgraph.ai"):
        self.base_url = base_url
    
    def html_to_text_nodes(self, html: str) -> dict:
        response = requests.post(
            f"{self.base_url}/html/to/text/nodes",
            json={"html": html}
        )
        return response.json()
    
    def reconstruct_with_mapping(self, html_dict: dict, hash_mapping: dict) -> str:
        response = requests.post(
            f"{self.base_url}/hashes/to/html",
            json={
                "html_dict": html_dict,
                "hash_mapping": hash_mapping
            }
        )
        return response.text

# Usage
client = HtmlServiceClient()
result = client.html_to_text_nodes("<html><body>Test</body></html>")
print(result["text_nodes"])
```

## Support

- **GitHub Issues:** [github.com/the-cyber-boardroom/MGraph-AI__Service__Html/issues](https://github.com/the-cyber-boardroom/MGraph-AI__Service__Html/issues)
- **Documentation:** [docs.mgraph.ai/services/html](https://docs.mgraph.ai/services/html)
- **Email:** support@mgraph.ai
