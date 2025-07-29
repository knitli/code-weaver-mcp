<!--
SPDX-FileCopyrightText: 2025 Knitli Inc.

SPDX-License-Identifier: MIT OR Apache-2.0
-->

# Intent Layer Architecture Diagram

## 🏗️ System Architecture Overview

```
                          ┌─────────────────────────────────────────────────────────────────┐
                          │                        LLM USER INTERFACE                      │
                          │                                                                 │
                          │   OLD: 4 tools → NEW: 1-2 intent-based tools                 │
                          │   ┌─────────────────┐    ┌─────────────────────────────────┐  │
                          │   │ process_intent  │    │ get_intent_capabilities         │  │
                          │   │ (main tool)     │    │ (optional helper)               │  │
                          │   └─────────────────┘    └─────────────────────────────────┘  │
                          └─────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                  INTENT LAYER (NEW)                                             │
    │                                                                                                 │
    │  ┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────────────────┐  │
    │  │ Intent Orchestrator │◄──►│   Intent Parser      │    │      Strategy Engine           │  │
    │  │ • Single entry point│    │ • Pattern matching   │    │ • Strategy selection           │  │
    │  │ • Result synthesis  │    │ • Confidence scoring │    │ • Performance tracking         │  │
    │  │ • Error recovery    │    │ • ML fallback        │    │ • Adaptive escalation          │  │
    │  └─────────────────────┘    └──────────────────────┘    └─────────────────────────────────┘  │
    │                ▲                         │                                │                     │
    │                │                         ▼                                ▼                     │
    │                │              ┌──────────────────────┐    ┌─────────────────────────────────┐  │
    │                │              │   ParsedIntent       │    │     Strategy Registry          │  │
    │                │              │ • intent_type        │    │ • SimpleSearchStrategy         │  │
    │                │              │ • primary_target     │    │ • AnalysisWorkflowStrategy     │  │
    │                │              │ • scope & complexity │    │ • IndexingStrategy             │  │
    │                │              │ • confidence score   │    │ • AdaptiveStrategy             │  │
    │                │              └──────────────────────┘    └─────────────────────────────────┘  │
    │                │                                                           │                     │
    │                │                                                           ▼                     │
    │                └─────────────────────────┬─────────────────┌─────────────────────────────────┐  │
    │                                          │                 │      Workflow Engine           │  │
    │                                          │                 │ • Multi-step execution         │  │
    │                                          │                 │ • Result aggregation           │  │
    │                                          │                 │ • Error handling               │  │
    │                                          │                 └─────────────────────────────────┘  │
    └─────────────────────────────────────────┼─────────────────────────────────────────────────────┘
                                              │
                                              ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                            EXISTING CODEWEAVER ARCHITECTURE                                    │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │                                SERVER LAYER                                             │  │
    │  │                                                                                         │  │
    │  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │  │
    │  │  │ index_codebase  │  │   search_code    │  │ ast_grep_search  │  │get_supported_   │  │  │
    │  │  │ _handler        │  │   _handler       │  │ _handler         │  │languages_handler│  │  │
    │  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────────┘  │  │
    │  │                                 ▲                                                       │  │
    │  │                                 │ Strategies call these directly                       │  │
    │  └─────────────────────────────────┼─────────────────────────────────────────────────────┘  │
    │                                    │                                                         │
    │  ┌─────────────────────────────────┼─────────────────────────────────────────────────────┐  │
    │  │                             SERVICES LAYER                                             │  │
    │  │                                 │                                                       │  │
    │  │  ┌─────────────────┐  ┌─────────▼────────┐  ┌──────────────────┐  ┌─────────────────┐  │  │
    │  │  │ ServicesManager │◄─┤ Service Context  │  │ Dependency       │  │ Health          │  │  │
    │  │  │ • Coordination  │  │ • Context inject  │  │ Injection        │  │ Monitoring      │  │  │
    │  │  │ • Lifecycle     │  │ • Service access  │  │ • Protocol-based │  │ • Auto-recovery │  │  │
    │  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────────┘  │  │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │                               MIDDLEWARE LAYER                                          │  │
    │  │                                                                                         │  │
    │  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │  │
    │  │  │ ChunkingMiddle  │  │ FileFiltering    │  │ RateLimiting     │  │ Logging         │  │  │
    │  │  │ ware            │  │ Middleware       │  │ Middleware       │  │ Middleware      │  │  │
    │  │  │ • AST-aware     │  │ • Gitignore      │  │ • Request limits │  │ • Structured    │  │  │
    │  │  │ • Language-spec │  │ • File patterns  │  │ • Backoff        │  │ • Performance   │  │  │
    │  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────────┘  │  │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │                                FACTORY LAYER                                            │  │
    │  │                                                                                         │  │
    │  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │  │
    │  │  │ Extensibility   │  │ BackendRegistry  │  │ SourceRegistry   │  │ ServiceRegistry │  │  │
    │  │  │ Manager         │  │ • Component disc │  │ • Data sources   │  │ • Service types │  │  │
    │  │  │ • Plugin system │  │ • Vector DBs     │  │ • File/Git/API   │  │ • Lifecycle mgmt│  │  │
    │  │  │ • Component mgmt│  │ • Provider APIs  │  │ • Custom sources │  │ • Health checks │  │  │
    │  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────────┘  │  │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │                           IMPLEMENTATION LAYER                                          │  │
    │  │                                                                                         │  │
    │  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │  │
    │  │  │ Providers       │  │ Backends         │  │ Sources          │  │ Services        │  │  │
    │  │  │ • VoyageAI      │  │ • Qdrant         │  │ • Filesystem     │  │ • Chunking      │  │  │
    │  │  │ • OpenAI        │  │ • Pinecone       │  │ • Git            │  │ • Filtering     │  │  │
    │  │  │ • Cohere        │  │ • Weaviate       │  │ • Database       │  │ • Validation    │  │  │
    │  │  │ • HuggingFace   │  │ • ChromaDB       │  │ • Custom         │  │ • Custom        │  │  │
    │  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────────┘  │  │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Intent Processing Flow Diagram

```
                    ┌─────────────────────────────────────────────────────────────────┐
                    │                      USER INPUT                                │
                    │              "understand authentication system"               │
                    └─────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              INTENT ORCHESTRATOR                                                │
    │                                                                                                 │
    │  1. Receive intent text                                                                         │
    │  2. Create service context                                                                      │
    │  3. Coordinate parsing → strategy → execution                                                   │
    │  4. Handle errors and fallbacks                                                                 │
    │  5. Return unified result                                                                       │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                               INTENT PARSER                                                     │
    │                                                                                                 │
    │  Input: "understand authentication system"                                                     │
    │                                                                                                 │
    │  Pattern Matching:                          ML Fallback (optional):                           │
    │  ┌─────────────────┐                       ┌─────────────────────────────────────────────┐   │
    │  │ • "understand" →│                       │ • Embedding similarity                     │   │
    │  │   UNDERSTAND    │                       │ • Intent classification model              │   │
    │  │ • "system" →    │                       │ • Confidence boosting                      │   │
    │  │   PROJECT scope │                       │ • Pattern learning                         │   │
    │  │ • "auth*" →     │                       └─────────────────────────────────────────────┘   │
    │  │   target entity │                                                                           │
    │  └─────────────────┘                                                                           │
    │                                                                                                 │
    │  Output: ParsedIntent {                                                                         │
    │    intent_type: UNDERSTAND,                                                                     │
    │    primary_target: "authentication system",                                                     │
    │    scope: PROJECT,                                                                              │
    │    complexity: COMPLEX,                                                                         │
    │    confidence: 0.8                                                                              │
    │  }                                                                                              │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              STRATEGY ENGINE                                                    │
    │                                                                                                 │
    │  Strategy Selection Matrix:                                                                     │
    │  ┌─────────────────────────────┬─────────────────────────────┬─────────────────────────────┐   │
    │  │       Strategy              │         Conditions          │         Score               │   │
    │  ├─────────────────────────────┼─────────────────────────────┼─────────────────────────────┤   │
    │  │ SimpleSearchStrategy        │ SEARCH + SIMPLE + conf>0.7  │ 0.3 (wrong intent)         │   │
    │  │ AnalysisWorkflowStrategy    │ UNDERSTAND + COMPLEX        │ 0.92 ✅ SELECTED           │   │
    │  │ IndexingStrategy            │ INDEX intent                │ 0.1 (wrong intent)         │   │
    │  │ AdaptiveStrategy            │ confidence < 0.6            │ 0.4 (high confidence)       │   │
    │  └─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘   │
    │                                                                                                 │
    │  Selected: AnalysisWorkflowStrategy (score: 0.92)                                              │
    │  Reason: UNDERSTAND intent + COMPLEX complexity + PROJECT scope                                │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                         ANALYSIS WORKFLOW STRATEGY                                             │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
    │  │                            WORKFLOW ENGINE                                              │   │
    │  │                                                                                         │   │
    │  │  Step 1: Initial Search                                                                 │   │
    │  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
    │  │  │ CALL: search_code_handler(                                                      │   │   │
    │  │  │   query="authentication system",                                                │   │   │
    │  │  │   limit=50,                                                                     │   │   │
    │  │  │   rerank=True                                                                   │   │   │
    │  │  │ )                                                                               │   │   │
    │  │  │ RESULT: 15 files, 6 directories, 3 languages                                   │   │   │
    │  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
    │  │                                      │                                                   │   │
    │  │                                      ▼                                                   │   │
    │  │  Step 2: Structural Analysis                                                             │   │
    │  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
    │  │  │ CALL: ast_grep_search_handler(                                                  │   │   │
    │  │  │   pattern="class $AUTH implements $INTERFACE",                                 │   │   │
    │  │  │   language="python",                                                           │   │   │
    │  │  │   root_path=detected_from_search                                               │   │   │
    │  │  │ )                                                                               │   │   │
    │  │  │ RESULT: 8 structural matches                                                    │   │   │
    │  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
    │  │                                      │                                                   │   │
    │  │                                      ▼                                                   │   │
    │  │  Step 3: Architecture Summary                                                            │   │
    │  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
    │  │  │ ANALYZE:                                                                        │   │   │
    │  │  │ • File relationships and dependencies                                           │   │   │
    │  │  │ • Component identification                                                      │   │   │
    │  │  │ • Pattern recognition across results                                            │   │   │
    │  │  │ • Generate comprehensive summary                                                │   │   │
    │  │  │ RESULT: Structured analysis with insights                                       │   │   │
    │  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
    │                                                                                                 │
    │  Uses Services: chunking_service, filtering_service, caching_service                           │
    │  Calls Tools: search_code_handler, ast_grep_search_handler                                     │
    │  Output: IntentResult with comprehensive analysis                                               │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                  INTENT RESULT                                                 │
    │                                                                                                 │
    │  {                                                                                              │
    │    "success": true,                                                                             │
    │    "data": {                                                                                    │
    │      "initial_search": { "result_count": 15, "top_files": [...] },                             │
    │      "structural_search": { "pattern_matches": 8, "language": "python" },                      │
    │      "summary": {                                                                               │
    │        "target": "authentication system",                                                       │
    │        "scope": "project",                                                                      │
    │        "key_findings": ["Multi-layer architecture", "Middleware integration", ...]             │
    │      }                                                                                          │
    │    },                                                                                           │
    │    "metadata": {                                                                                │
    │      "workflow": "multi_step_analysis",                                                         │
    │      "strategy": "analysis_workflow",                                                           │
    │      "execution_time": 3.2,                                                                     │
    │      "services_used": ["chunking", "filtering", "caching"]                                     │
    │    }                                                                                            │
    │  }                                                                                              │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🎛️ Strategy Selection Decision Tree

```
                                    ┌─────────────────────────────────────┐
                                    │           ParsedIntent              │
                                    │ • intent_type: UNDERSTAND          │
                                    │ • complexity: COMPLEX               │
                                    │ • scope: PROJECT                    │
                                    │ • confidence: 0.8                   │
                                    └─────────────────────────────────────┘
                                                      │
                                                      ▼
                                    ┌─────────────────────────────────────┐
                                    │        Strategy Evaluation         │
                                    └─────────────────────────────────────┘
                                                      │
                      ┌───────────────────────────────┼───────────────────────────────┐
                      │                               │                               │
                      ▼                               ▼                               ▼
        ┌─────────────────────────┐    ┌─────────────────────────┐    ┌─────────────────────────┐
        │   SimpleSearchStrategy  │    │ AnalysisWorkflowStrategy│    │    AdaptiveStrategy     │
        │                         │    │                         │    │                         │
        │ Conditions:             │    │ Conditions:             │    │ Conditions:             │
        │ • intent=SEARCH ❌      │    │ • intent=UNDERSTAND ✅  │    │ • confidence<0.6 ❌     │
        │ • complexity=SIMPLE ❌  │    │ • complexity=COMPLEX ✅ │    │ • fallback needed ❌    │
        │ • confidence>0.7 ✅     │    │ • scope=PROJECT ✅      │    │                         │
        │                         │    │                         │    │ Score: 0.4             │
        │ Score: 0.3              │    │ Score: 0.92 🎯          │    │ Rank: 3rd              │
        │ Rank: 2nd               │    │ Rank: 1st               │    │                         │
        └─────────────────────────┘    └─────────────────────────┘    └─────────────────────────┘
                      │                               │                               │
                      └───────────────────────────────┼───────────────────────────────┘
                                                      │
                                                      ▼
                                    ┌─────────────────────────────────────┐
                                    │     SELECTED STRATEGY               │
                                    │  AnalysisWorkflowStrategy           │
                                    │                                     │
                                    │ Execution Plan:                     │
                                    │ 1. Enhanced search operation        │
                                    │ 2. Structural pattern analysis      │
                                    │ 3. Component relationship mapping   │
                                    │ 4. Summary generation               │
                                    │                                     │
                                    │ Estimated time: 3-5 seconds         │
                                    │ Resource usage: Medium              │
                                    │ Services needed: All available      │
                                    └─────────────────────────────────────┘
```

### Simple Intent Flow Example

**User Input**: "find authentication functions"

```
Flow: Simple Search Strategy
┌─────────────────────────────────────────────────────────────┐
│ 1. Intent Parser                                           │
│    Input: "find authentication functions"                  │
│    Output: ParsedIntent {                                  │
│      intent_type: SEARCH,                                  │
│      primary_target: "authentication functions",           │
│      scope: MODULE,                                        │
│      complexity: SIMPLE,                                   │
│      confidence: 0.9                                       │
│    }                                                       │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Strategy Engine                                         │
│    Selected: SimpleSearchStrategy (score: 0.95)            │
│    Reason: High confidence + SEARCH intent + SIMPLE        │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Simple Search Strategy Execution                        │
│    Direct mapping to: search_code_handler(                 │
│      query="authentication functions",                     │
│      limit=10,                                            │
│      rerank=True                                           │
│    )                                                       │
│    Execution time: 0.8s                                   │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. User Response                                           │
│    {                                                       │
│      "success": true,                                      │
│      "data": {                                             │
│        "results": [8 code snippets],                       │
│        "query": "authentication functions",                │
│        "result_count": 8                                   │
│      },                                                    │
│      "metadata": {                                         │
│        "workflow": "direct_search",                        │
│        "strategy": "simple_search"                         │
│      }                                                     │
│    }                                                       │
└─────────────────────────────────────────────────────────────┘
```

### Complex Intent Flow Example

**User Input**: "understand the complete authentication system architecture"

```
Flow: Analysis Workflow Strategy
┌─────────────────────────────────────────────────────────────┐
│ 1. Intent Parser                                           │
│    Input: "understand the complete authentication system   │
│           architecture"                                    │
│    Output: ParsedIntent {                                  │
│      intent_type: UNDERSTAND,                              │
│      primary_target: "authentication system architecture", │
│      scope: PROJECT,                                       │
│      complexity: COMPLEX,                                  │
│      confidence: 0.8                                       │
│    }                                                       │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Strategy Engine                                         │
│    Selected: AnalysisWorkflowStrategy (score: 0.92)        │
│    Reason: UNDERSTAND intent + COMPLEX + PROJECT scope     │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Multi-Step Analysis Workflow                           │
│                                                           │
│    Step 1: Initial Search                                 │
│    ├─ search_code("authentication system architecture")    │
│    ├─ Result: 15 files across 6 directories              │
│    └─ Languages: Python, JavaScript, TypeScript          │
│                                                           │
│    Step 2: Structural Analysis                           │
│    ├─ Detect patterns in results                         │
│    ├─ ast_grep_search for auth patterns in Python        │
│    └─ Result: 8 structural matches                       │
│                                                           │
│    Step 3: Architecture Summary                          │
│    ├─ Analyze file relationships                         │
│    ├─ Identify key components                            │
│    └─ Generate comprehensive summary                     │
│                                                           │
│    Total execution time: 3.2s                            │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Comprehensive User Response                            │
│    {                                                       │
│      "success": true,                                      │
│      "data": {                                             │
│        "initial_search": {                                 │
│          "result_count": 15,                               │
│          "top_files": [                                    │
│            "auth/models.py",                               │
│            "auth/views.py",                                │
│            "middleware/auth.py"                            │
│          ]                                                 │
│        },                                                  │
│        "structural_search": {                              │
│          "pattern_matches": 8,                             │
│          "language": "python"                              │
│        },                                                  │
│        "summary": {                                        │
│          "target": "authentication system architecture",   │
│          "scope": "project",                               │
│          "total_results": 15,                              │
│          "affected_directories": 6,                        │
│          "languages_involved": ["python", "javascript"],   │
│          "key_findings": [                                 │
│            "Widely used throughout codebase",              │
│            "Multi-layer architecture with middleware",     │
│            "Separation of models and views"                │
│          ]                                                 │
│        }                                                   │
│      },                                                    │
│      "metadata": {                                         │
│        "workflow": "multi_step_analysis",                  │
│        "workflow_steps": [                                 │
│          "initial_search",                                 │
│          "structural_search",                              │
│          "summary_generation"                              │
│        ],                                                  │
│        "strategy": "analysis_workflow"                     │
│      }                                                     │
│    }                                                       │
└─────────────────────────────────────────────────────────────┘
```

### Adaptive Intent Flow Example

**User Input**: "jwt stuff" (Low confidence input)

```
Flow: Adaptive Strategy with Escalation
┌─────────────────────────────────────────────────────────────┐
│ 1. Intent Parser                                           │
│    Input: "jwt stuff"                                      │
│    Output: ParsedIntent {                                  │
│      intent_type: SEARCH (fallback),                       │
│      primary_target: "jwt stuff",                          │
│      scope: MODULE,                                        │
│      complexity: ADAPTIVE,                                 │
│      confidence: 0.4 (low)                                │
│    }                                                       │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Strategy Engine                                         │
│    Selected: AdaptiveStrategy (score: 0.7)                 │
│    Reason: Low confidence triggers adaptive approach       │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Adaptive Strategy Execution                            │
│                                                           │
│    Phase 1: Try Simple Search                            │
│    ├─ SimpleSearchStrategy.execute("jwt stuff")           │
│    ├─ Result: 2 results found                            │
│    └─ Assessment: Insufficient results (<3)               │
│                                                           │
│    Phase 2: Escalate to Analysis                         │
│    ├─ Switch to AnalysisWorkflowStrategy                  │
│    ├─ Enhanced search with "jwt token authentication"     │
│    ├─ Include structural patterns                        │
│    └─ Result: 8 comprehensive results                    │
│                                                           │
│    Total execution time: 2.1s                            │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Adaptive User Response                                 │
│    {                                                       │
│      "success": true,                                      │
│      "data": {                                             │
│        "enhanced_results": [8 jwt-related snippets],       │
│        "original_query": "jwt stuff",                      │
│        "enhanced_query": "jwt token authentication",       │
│        "escalation_reason": "Insufficient initial results" │
│      },                                                    │
│      "metadata": {                                         │
│        "workflow": "adaptive_escalation",                  │
│        "strategy": "adaptive",                             │
│        "escalation_path": "simple → analysis",             │
│        "confidence_improvement": "0.4 → 0.8"               │
│      }                                                     │
│    }                                                       │
└─────────────────────────────────────────────────────────────┘
```

## 7. Summary and Benefits

### Architecture Benefits

1. **Simplified LLM Interface**: Reduces 4 tools to 1-2 natural language tools
2. **Intelligent Orchestration**: Auto-selects appropriate workflows based on intent
3. **Preserves Extensibility**: Developers can add custom strategies and configure behavior
4. **Graceful Degradation**: Multiple fallback mechanisms for error recovery
5. **Performance Optimization**: Strategy selection based on success rates and execution time
6. **iPhone-like Experience**: "Just works" for users, powerful for developers

### Developer Configurability

- **Strategy Registration**: Plugin system for custom intent strategies
- **Parser Customization**: Custom patterns and ML fallbacks
- **Workflow Configuration**: Adjustable complexity thresholds and execution parameters
- **Debug Mode**: Expose internal tools and strategy debugging
- **Performance Tuning**: Strategy performance tracking and optimization

### Integration Points

- **Services Layer**: Leverages existing ServicesManager for dependency injection
- **Factory System**: Uses ExtensibilityManager for component discovery
- **Middleware**: Integrates with FastMCP middleware stack
- **Configuration**: Extends existing configuration system with intent-specific settings
- **Error Handling**: Builds on existing error patterns with intent-aware recovery

The intent layer provides a transformative user experience while maintaining the robust, extensible architecture that makes CodeWeaver powerful for developers. It bridges the gap between complex technical capabilities and intuitive user interaction, following the established CodeWeaver patterns for protocols, dependency injection, and configuration management.