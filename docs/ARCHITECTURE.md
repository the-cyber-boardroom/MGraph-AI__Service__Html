# Architecture Diagram - MGraph-AI__Service__Html

## Service Architecture Overview

```
┌───────────────────────────────────────────────────────────────────┐
│                         CLIENT APPLICATION                        │
│                   (Mitmproxy, Web App, etc.)                      │
└────────────────────────────────┬──────────────────────────────────┘
                                 │
                                 │ HTTP(S)
                                 ▼
┌───────────────────────────────────────────────────────────────────┐
│                    API Gateway / Load Balancer                    │
└────────────────────────────────┬──────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│              MGraph-AI__Service__Html (THIS SERVICE)               │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                  Html__Fast_API                          │    │
│  │                (Main Application)                        │    │
│  └────────────┬──────────────┬──────────────┬──────────────┘    │
│               │              │              │                    │
│        ┌──────▼─────┐  ┌────▼────┐  ┌─────▼──────┐             │
│        │ Routes__   │  │ Routes__│  │ Routes__   │             │
│        │   Html     │  │   Dict  │  │  Hashes    │             │
│        │            │  │         │  │            │             │
│        │ 6 endpoints│  │3 endpts │  │ 1 endpoint │             │
│        └──────┬─────┘  └────┬────┘  └─────┬──────┘             │
│               │              │              │                    │
│               └──────────────┼──────────────┘                    │
│                              │                                   │
│                    ┌─────────▼──────────┐                        │
│                    │  Html__Direct__    │                        │
│                    │  Transformations   │                        │
│                    │                    │                        │
│                    │  Core Logic:       │                        │
│                    │  • html ↔ dict    │                        │
│                    │  • text extraction │                        │
│                    │  • formatting      │                        │
│                    └─────────┬──────────┘                        │
│                              │                                   │
│                    ┌─────────▼──────────┐                        │
│                    │  Html__Extract__   │                        │
│                    │    Text_Nodes      │                        │
│                    │                    │                        │
│                    │  • Tree traversal  │                        │
│                    │  • Hash generation │                        │
│                    │  • Text capture    │                        │
│                    └────────────────────┘                        │
│                                                                  │
└────────────────────────────────────────────────────────────────────┘
```

## Data Flow Patterns

### Pattern 1: Simple Text Extraction

```
Client sends HTML
       │
       ▼
POST /html/to/text/nodes
       │
       ├─► html__to__html_dict()
       │   (Parse HTML)
       │
       ├─► html_dict__to__text_nodes()
       │   (Extract text with hashes)
       │
       └─► Response: {text_nodes: {...}}
```

### Pattern 2: Cached Processing (Atomic)

```
Step 1: Parse and Cache
Client sends HTML
       │
       ▼
POST /html/to/dict
       │
       ├─► html__to__html_dict()
       │
       └─► Response: {html_dict: {...}}
                │
                ▼
          Cache Service
          (Store for 1 hour)

Step 2: Extract Text (from cache)
Client sends html_dict
       │
       ▼
POST /dict/to/text/nodes
       │
       ├─► html_dict__to__text_nodes()
       │
       └─► Response: {text_nodes: {...}}
                │
                ▼
          Cache Service
          (Store indefinitely)
```

### Pattern 3: Full Pipeline with External Service

```
┌─────────────────────────────────────────────────────────┐
│ Client Application                                      │
└───────────┬─────────────────────────────────────────────┘
            │
            │ 1. HTML Content
            ▼
┌───────────────────────────────────────────────────────┐
│ MGraph-AI__Service__Html                              │
│                                                       │
│ POST /html/to/dict                                    │
│   └─► {html_dict: {...}}                             │
└───────────┬───────────────────────────────────────────┘
            │
            │ 2. html_dict (cached)
            ▼
┌───────────────────────────────────────────────────────┐
│ MGraph-AI__Service__Html                              │
│                                                       │
│ POST /dict/to/text/nodes                              │
│   └─► {text_nodes: {hash1: {text: "..."}, ...}}      │
└───────────┬───────────────────────────────────────────┘
            │
            │ 3. text_nodes
            ▼
┌───────────────────────────────────────────────────────┐
│ MGraph-AI__Service__Semantic_Text                     │
│                                                       │
│ POST /text/to/ratings                                 │
│   └─► {ratings: {hash1: 0.8, hash2: 0.3, ...}}       │
└───────────┬───────────────────────────────────────────┘
            │
            │ 4. ratings
            ▼
┌───────────────────────────────────────────────────────┐
│ Client creates hash_mapping                           │
│   {hash1: "[Positive] text", hash2: "xxxxx", ...}    │
└───────────┬───────────────────────────────────────────┘
            │
            │ 5. html_dict + hash_mapping
            ▼
┌───────────────────────────────────────────────────────┐
│ MGraph-AI__Service__Html                              │
│                                                       │
│ POST /hashes/to/html                                  │
│   └─► Modified HTML (text/html)                      │
└───────────┬───────────────────────────────────────────┘
            │
            │ 6. Filtered HTML
            ▼
┌───────────────────────────────────────────────────────┐
│ Client Application                                    │
│   (Display/Use filtered content)                      │
└───────────────────────────────────────────────────────┘
```

## Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────┐
│                    Routes Layer                            │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Routes__Html │  │ Routes__Dict │  │Routes__Hashes│    │
│  │              │  │              │  │              │    │
│  │ • to__dict   │  │ • to__html   │  │ • to__html   │    │
│  │ • to__html   │  │ • to__text.. │  │   (with      │    │
│  │ • to__text.. │  │ • to__lines  │  │    mapping)  │    │
│  │ • to__lines  │  └──────┬───────┘  └──────┬───────┘    │
│  │ • to__html_  │         │                 │            │
│  │   hashes     │         │                 │            │
│  │ • to__html_  │         │                 │            │
│  │   xxx        │         │                 │            │
│  └──────┬───────┘         │                 │            │
│         │                 │                 │            │
└─────────┼─────────────────┼─────────────────┼────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│              Html__Direct__Transformations                 │
│                                                            │
│  • html__to__html_dict()      ─┐                          │
│  • html_dict__to__html()       ├─ Core Operations         │
│  • html__to__lines()           │                          │
│  • html_dict__to__text_nodes() ┘                          │
│                                                            │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│              Html__Extract_Text_Nodes                      │
│                                                            │
│  • extract_from_html_dict()    ─┐                         │
│  • traverse()                   ├─ Text Extraction        │
│  • capture_text()               │                         │
│  • create_html_with_hashes()    │                         │
│  • create_html_with_xxx()       ┘                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│           OSBot-Utils HTML Transformers                    │
│                                                            │
│  • Html__To__Html_Dict         (parsing)                  │
│  • Html_Dict__To__Html         (reconstruction)           │
│  • Html__To__Html_Document     (document structure)       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Request/Response Schema Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Schema Layer                             │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Schema__Html__To__Dict                     │    │
│  │  Request:  Safe_Str__Html                          │    │
│  │  Response: Dict, Safe_UInt, Safe_UInt              │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │      Schema__Html__To__Text__Nodes                 │    │
│  │  Request:  Safe_Str__Html, Safe_UInt (max_depth)   │    │
│  │  Response: Dict[Safe_Str__Hash, Dict], Safe_UInt   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │      Schema__Hashes__To__Html__Request             │    │
│  │  Request:  Dict (html_dict), Dict[Hash, str]       │    │
│  │  Response: HTMLResponse                            │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Type_Safe Validation
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Type_Safe Runtime Checking                     │
│                                                             │
│  • Validates all Safe_* types                               │
│  • Converts inputs to proper types                          │
│  • Catches type errors at assignment                        │
│  • Ensures data integrity                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                        │
│                                                             │
│  mgraph_ai_service_html/                                    │
│    ├─ html__fast_api/                                       │
│    ├─ lambdas/lambda_handler.py                            │
│    ├─ tests/                                                │
│    └─ setup.py                                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ CI/CD Pipeline
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AWS Lambda Function                       │
│                                                             │
│  Function Name: mgraph-ai-service-html                      │
│  Runtime: Python 3.11                                       │
│  Handler: lambda_handler.run                                │
│  Memory: 512 MB                                             │
│  Timeout: 30s                                               │
│                                                             │
│  Dependencies:                                              │
│    • osbot-fast-api-serverless                              │
│    • memory-fs                                              │
│    • osbot-utils                                            │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway (REST API)                     │
│                                                             │
│  Endpoint: https://html.mgraph.ai                           │
│                                                             │
│  Routes:                                                    │
│    /html/*     → Lambda Integration                         │
│    /dict/*     → Lambda Integration                         │
│    /hashes/*   → Lambda Integration                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Security & Performance

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
│                                                             │
│  1. API Gateway                                             │
│     • Rate limiting (100 req/min)                           │
│     • API key authentication                                │
│     • Request validation                                    │
│                                                             │
│  2. Type_Safe Validation                                    │
│     • Input sanitization                                    │
│     • Safe_Str__Html (1MB limit)                            │
│     • Safe_UInt bounds checking                             │
│                                                             │
│  3. Lambda Execution                                        │
│     • Isolated environment                                  │
│     • No persistent state                                   │
│     • Automatic scaling                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Key Architectural Principles:**

1. **Stateless** - No server-side state or caching
2. **Type-Safe** - Runtime validation at all layers
3. **Modular** - Clear separation of concerns
4. **Scalable** - AWS Lambda auto-scaling
5. **Fast** - Pure HTML ops, no AI/LLM delays
6. **Testable** - Every component independently testable
