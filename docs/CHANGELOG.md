# Changelog

All notable changes to MGraph-AI__Service__Html will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Batch processing endpoints
- WebSocket support for streaming operations
- Additional output formats (Markdown, Plain Text)
- Performance metrics endpoint
- Health check with detailed diagnostics

## [0.1.0] - 2025-10-15

### Added
- Initial release of MGraph-AI__Service__Html
- Core HTML transformation operations:
  - `Html__Direct__Transformations` - Pure HTML processing
  - `Html__Extract_Text_Nodes` - Text node extraction with hashing
- Type_Safe schemas for all requests/responses
- Three main route groups:
  - `Routes__Html` - HTML → various transformations
  - `Routes__Dict` - html_dict → various outputs
  - `Routes__Hashes` - Hash-based reconstruction
- Atomic operations:
  - `/html/to/dict` - Parse HTML to dict
  - `/html/to/html` - Round-trip validation
- Compound operations:
  - `/html/to/text/nodes` - One-shot text extraction
  - `/html/to/lines` - Human-readable output
  - `/html/to/html/hashes` - Visual debug with hashes
  - `/html/to/html/xxx` - Privacy masking
- Hash reconstruction endpoint: `/hashes/to/html`
- AWS Lambda deployment support
- Complete test suite with pytest
- Comprehensive documentation:
  - README.md with architecture overview
  - API_DOCS.md with endpoint specifications
  - Inline code documentation

### Design Decisions
- **No LLM Dependencies** - Kept service pure and fast
- **No Built-in Caching** - Delegated to caller for flexibility
- **Type_Safe Throughout** - Runtime type checking on all operations
- **Atomic & Compound APIs** - Maximum control for callers
- **Schema-Only Data Structures** - No business logic in schemas

### Infrastructure
- FastAPI application with Serverless support
- AWS Lambda handler with dependency management
- Deployment utilities for easy Lambda deployment
- Version management system

### Testing
- Unit tests for routes, core components, and schemas
- Test client setup for FastAPI routes
- Pytest configuration with coverage support

### Dependencies
- osbot-utils >= 1.90.0
- osbot-fast-api >= 1.19.0
- osbot-fast-api-serverless >= 1.19.0
- memory-fs >= 0.24.0

## Release Notes

### v0.1.0 - "Foundation Release"

This initial release establishes the core architecture for HTML structural transformation. The service is designed as part of the MGraph-AI ecosystem, specifically separating HTML structural operations from semantic text analysis.

**Key Features:**
1. **Pure HTML Processing** - No semantic analysis, LLM calls, or AI operations
2. **Flexible Caching Strategy** - Callers control caching via Cache Service
3. **Hash-Based Content Addressing** - Stable identifiers for text nodes
4. **Round-Trip Validation** - Quality assurance built into API

**Breaking Changes from WCF:**
- Removed all LLM-related endpoints
- Removed URL-based operations (callers fetch HTML)
- Removed built-in caching
- New endpoint structure with `/html/`, `/dict/`, `/hashes/` prefixes

**Migration Path:**
- Old `/html-graphs/url-to-html` → Caller fetches HTML + `/html/to/dict`
- Old `/html-graphs/url-to-ratings` → Separate Semantic_Text service
- Old internal caching → Use Cache Service explicitly

**Known Limitations:**
- No batch processing yet
- Max depth limited to 256 by default
- No compression support yet
- Single-threaded processing only

**Next Steps:**
- Integration testing with Cache Service
- Integration testing with Semantic_Text Service
- Performance benchmarking
- Production deployment to AWS Lambda
- API Gateway configuration
