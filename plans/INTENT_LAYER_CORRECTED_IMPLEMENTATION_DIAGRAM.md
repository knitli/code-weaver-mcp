<!--
SPDX-FileCopyrightText: 2025 Knitli Inc.

SPDX-License-Identifier: MIT OR Apache-2.0
-->

# Intent Layer: Corrected Implementation Architecture Diagram

## 🏗️ Architecture-Compliant System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    LLM USER INTERFACE                                  │
│                                                                                         │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────────────────┐ │
│  │         process_intent          │    │        get_intent_capabilities              │ │
│  │                                 │    │                                             │ │
│  │ Natural Language Input:         │    │ Returns:                                    │ │
│  │ • "find auth functions"         │    │ • Supported intent types (NO INDEX)       │ │
│  │ • "understand db architecture"  │    │ • Example queries                          │ │
│  │ • "analyze performance issues"  │    │ • Available strategies                     │ │
│  └─────────────────────────────────┘    └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        INTENT LAYER (ARCHITECTURE COMPLIANT)                          │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                    INTENT ORCHESTRATOR SERVICE                                    │ │
│  │                   📍 EXTENDS BaseServiceProvider                                  │ │
│  │                                                                                   │ │
│  │  class IntentOrchestrator(BaseServiceProvider):                                  │ │
│  │      async def process_intent(intent_text, context) -> IntentResult              │ │
│  │      async def health_check() -> ServiceHealth                                   │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │ │
│  │  │ Service Context │  │ Intent Parsing  │  │ Strategy        │  │ Result      │ │ │
│  │  │ Injection       │  │ • Pattern match │  │ Selection       │  │ Caching     │ │ │
│  │  │ • Existing      │  │ • Confidence    │  │ • Performance   │  │ • Service   │ │ │
│  │  │   patterns      │  │ • Error handle  │  │ • Registry      │  │   cache     │ │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                          │                                             │
│                                          ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │              PARSING LAYER (EXTENDS EXISTING PATTERNS)                           │ │
│  │                                                                                   │ │
│  │  ┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐ │ │
│  │  │         Pattern Matcher             │  │      NLP Enhanced Parser            │ │ │
│  │  │         📍 ESSENTIAL                │  │      📍 ENHANCEMENT                 │ │ │
│  │  │                                     │  │                                     │ │ │
│  │  │ Intent Recognition (NO INDEX):      │  │ spaCy Pipeline (NO INDEX):          │ │ │
│  │  │ • "find" → SEARCH                  │  │ • Enhanced classification            │ │ │
│  │  │ • "understand" → UNDERSTAND         │  │ • Domain models                     │ │ │
│  │  │ • "analyze" → ANALYZE               │  │ • Entity recognition                │ │ │
│  │  │ • AUTO-INDEXING: Background only    │  │ • Confidence scoring                │ │ │
│  │  │                                     │  │                                     │ │ │
│  │  │ ParsedIntent Output:                │  │ Enhanced ParsedIntent:              │ │ │
│  │  │ • intent_type: SEARCH|UNDERSTAND|   │  │ • Higher confidence scores          │ │ │
│  │  │   ANALYZE (never INDEX)             │  │ • Semantic understanding            │ │ │
│  │  │ • primary_target: extracted entity  │  │ • Context preservation              │ │ │
│  │  │ • scope: FILE|MODULE|PROJECT        │  │ • Advanced metadata                 │ │ │
│  │  │ • complexity: assessment            │  │                                     │ │ │
│  │  │ • confidence: 0.0-1.0 score         │  │                                     │ │ │
│  │  └─────────────────────────────────────┘  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                          │                                             │
│                                          ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │           STRATEGY ENGINE (EXTENSIBILITY MANAGER INTEGRATION)                     │ │
│  │                                                                                   │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                       Strategy Registry                                     │ │ │
│  │  │                📍 INTEGRATED with ExtensibilityManager                     │ │ │
│  │  │                                                                             │ │ │
│  │  │  Plugin Discovery → Strategy Registration → Performance Tracking           │ │ │
│  │  │                             │                                               │ │ │
│  │  │         ┌───────────────────┼───────────────────┐                          │ │ │
│  │  │         │                   │                   │                          │ │ │
│  │  │         ▼                   ▼                   ▼                          │ │ │
│  │  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐              │ │ │
│  │  │  │ SimpleSearch    │ │ AnalysisWorkflow│ │ Adaptive        │              │ │ │
│  │  │  │ Strategy        │ │ Strategy        │ │ Strategy        │              │ │ │
│  │  │  │ 📍 BaseServiceProvider📍 BaseServiceProvider📍 BaseServiceProvider│     │ │ │
│  │  │  │                 │ │                 │ │                 │              │ │ │
│  │  │  │ Handles:        │ │ Handles:        │ │ Handles:        │              │ │ │
│  │  │  │ • SEARCH intent │ │ • UNDERSTAND    │ │ • Fallback      │              │ │ │
│  │  │  │ • SIMPLE        │ │ • COMPLEX       │ │ • Low confidence│              │ │ │
│  │  │  │ • High confidence│ │ • PROJECT scope │ │ • Error recovery│              │ │ │
│  │  │  │                 │ │                 │ │                 │              │ │ │
│  │  │  │ Service Context:│ │ Service Context:│ │ Service Context:│              │ │ │
│  │  │  │ • Inherited     │ │ • Inherited     │ │ • Inherited     │              │ │ │
│  │  │  │ • Health checks │ │ • Multi-step    │ │ • Escalation    │              │ │ │
│  │  │  └─────────────────┘ └─────────────────┘ └─────────────────┘              │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    SERVICE BRIDGE INTEGRATION (EXISTING PATTERNS)                     │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                      IntentServiceBridge(ServiceBridge)                           │ │
│  │                     📍 EXTENDS EXISTING ServiceBridge                             │ │
│  │                                                                                   │ │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────┐ │ │
│  │  │   Service   │→  │  Intent     │→  │  Context    │→  │   Tool      │→  │Resp │ │ │
│  │  │ Context     │   │ Processing  │   │ Enhancement │   │  Execution  │   │onse │ │ │
│  │  │ Creation    │   │ Routing     │   │ (existing)  │   │ (existing)  │   │     │ │ │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────┘ │ │
│  │         │                  │                 │                 │              │   │ │
│  │         ▼                  ▼                 ▼                 ▼              ▼   │ │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────┐ │ │
│  │  │ Existing    │   │ Intent      │   │ Existing    │   │ Existing    │   │Exist│ │ │
│  │  │ Service     │   │ Orchestrator│   │ Middleware  │   │ Performance │   │ing  │ │ │
│  │  │ Injection   │   │ Service     │   │ Pipeline    │   │ Monitoring  │   │Error│ │ │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         EXISTING CODEWEAVER ARCHITECTURE                               │
│                           📍 NO CHANGES - ENHANCED ONLY                                │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          SERVICES MANAGER (ENHANCED)                              │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ ServicesManager │  │ AutoIndexing     │  │ Intent           │  │ Health      │ │ │
│  │  │ • Coordination  │  │ Service          │  │ Orchestrator     │  │ Monitoring  │ │ │
│  │  │ • Lifecycle     │  │ 📍 NEW SERVICE   │  │ 📍 NEW SERVICE   │  │ 📍 ENHANCED │ │ │
│  │  │ • Dependencies  │  │                  │  │                  │  │             │ │ │
│  │  │                 │ ◄┤ Background:      │  │ LLM Interface:   │  │ All services│ │ │
│  │  │ Enhanced for:   │  │ • File watching  │  │ • Intent process │  │ monitored   │ │ │
│  │  │ • Intent services│  │ • Auto-indexing  │  │ • Natural lang   │  │ • Recovery  │ │ │
│  │  │ • Background svc │  │ • NOT for LLMs   │  │ • For LLMs only  │  │ • Alerting  │ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          EXTENSIBILITY MANAGER (ENHANCED)                         │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ Plugin          │  │ Service          │  │ Strategy         │  │ Component   │ │ │
│  │  │ Discovery       │  │ Registry         │  │ Registry         │  │ Lifecycle   │ │ │
│  │  │ • Entry points  │  │ 📍 ENHANCED      │  │ 📍 NEW           │  │ • Health    │ │ │
│  │  │ • Directory scan│  │                  │  │                  │  │ • Validation│ │ │
│  │  │ • Module intro  │  │ New services:    │  │ Intent strategies│  │ • Recovery  │ │ │
│  │  │                 │  │ • Intent orch.   │  │ • Discovery      │  │             │ │ │
│  │  │ Enhanced for:   │  │ • Auto-indexing  │  │ • Registration   │  │ Enhanced:   │ │ │
│  │  │ • Intent strat. │  │ • Strategy reg.  │  │ • Performance    │  │ • Intent    │ │ │
│  │  │ • Parser plugins│  │ • Health track   │  │ • Selection      │  │   lifecycle │ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SERVER LAYER (SAME)                                  │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ search_code     │  │ ast_grep_search  │  │get_supported     │  │ NO INDEX    │ │ │
│  │  │ _handler        │  │ _handler         │  │_languages        │  │ TOOL        │ │ │
│  │  │                 │  │                  │  │ _handler         │  │             │ │ │
│  │  │ Used by:        │  │ Used by:         │  │                  │  │ Index tool  │ │ │
│  │  │ • SimpleSearch  │  │ • AnalysisFlow   │  │ Used by:         │  │ REMOVED     │ │ │
│  │  │ • All strategies│  │ • Structural     │  │ • All strategies │  │             │ │ │
│  │  │ • Same interface│  │ • Same interface │  │ • Capability     │  │ Instead:    │ │ │
│  │  │                 │  │                  │  │   queries        │  │ Background  │ │ │
│  │  │                 │  │                  │  │                  │  │ AutoIndexing│ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                           MIDDLEWARE LAYER (SAME)                                 │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ ChunkingMiddle  │  │ FileFiltering    │  │ RateLimiting     │  │ Logging     │ │ │
│  │  │ ware            │  │ Middleware       │  │ Middleware       │  │ Middleware  │ │ │
│  │  │ 📍 USED BY      │  │ 📍 USED BY       │  │ 📍 USED BY       │  │ 📍 USED BY  │ │ │
│  │  │ AutoIndexing    │  │ AutoIndexing     │  │ Intent strategies│  │ All intent  │ │ │
│  │  │                 │  │                  │  │                  │  │ operations  │ │ │
│  │  │ Intent Usage:   │  │ Intent Usage:    │  │ Intent Usage:    │  │ Intent:     │ │ │
│  │  │ • Result chunk  │  │ • File discovery │  │ • Intent limits  │  │ • Intent    │ │ │
│  │  │ • Context build │  │ • Context filter │  │ • Strategy limits│  │   tracking  │ │ │
│  │  │ • Service inject│  │ • Background idx │  │ • Service limits │  │ • Performance│ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          FACTORY LAYER (SAME)                                     │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ CodeWeaver      │  │ BackendRegistry  │  │ SourceRegistry   │  │ Service     │ │ │
│  │  │ Factory         │  │ • Vector DBs     │  │ • Data sources   │  │ Registry    │ │ │
│  │  │ • Component     │  │ • Provider APIs  │  │ • File/Git/API   │  │ 📍 ENHANCED │ │ │
│  │  │   creation      │  │ • Embeddings     │  │ • Custom sources │  │             │ │ │
│  │  │ • Dependencies  │  │                  │  │                  │  │ New services│ │ │
│  │  │                 │  │ Same             │  │ Same             │  │ • Intent    │ │ │
│  │  │ Same            │  │                  │  │                  │  │ • AutoIndex │ │ │
│  │  │                 │  │                  │  │                  │  │ • Strategy  │ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          IMPLEMENTATION LAYER (SAME)                              │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ Providers       │  │ Backends         │  │ Sources          │  │ Services    │ │ │
│  │  │ • VoyageAI      │  │ • Qdrant         │  │ • Filesystem     │  │ 📍 ENHANCED │ │ │
│  │  │ • OpenAI        │  │ • Pinecone       │  │ • Git            │  │             │ │ │
│  │  │ • Cohere        │  │ • Weaviate       │  │ • Database       │  │ New:        │ │ │
│  │  │ • HuggingFace   │  │ • ChromaDB       │  │ • Custom         │  │ • Intent    │ │ │
│  │  │                 │  │                  │  │                  │  │ • AutoIndex │ │ │
│  │  │ Same            │  │ Same             │  │ Same             │  │ • Caching   │ │ │
│  │  │                 │  │                  │  │                  │  │ • Strategy  │ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Auto-Indexing Background Service Flow

```
                    ┌─────────────────────────────────────────────────────────────────┐
                    │                    FRAMEWORK DEVELOPER                         │
                    │           (Controls indexing - NOT LLM users)                  │
                    └─────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              AUTO-INDEXING SERVICE                                              │
    │                      📍 AutoIndexingService(BaseServiceProvider)                               │
    │                                                                                                 │
    │  Developer Controls (NOT exposed to LLMs):                                                     │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
    │  │ Start Monitoring│ ── │ Stop Monitoring │ ── │ Health Check    │ ── │ Service Status  │      │
    │  │ • Path watching │    │ • Clean shutdown│    │ • Monitor health│    │ • Performance   │      │
    │  │ • Initial index │    │ • Resource clean│    │ • Error detect  │    │ • Resource use  │      │
    │  │ • File patterns │    │ • State persist │    │ • Service deps  │    │ • Index status  │      │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘      │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                            BACKGROUND PROCESSING PIPELINE                                      │
    │                                                                                                 │
    │  File System Events → Debounce → Filter → Chunk → Index → Update                               │
    │                                                                                                 │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
    │  │ File Watcher    │ ── │ Change Filter   │ ── │ Content Chunking│ ── │ Vector Storage  │      │
    │  │ • watchdog      │    │ • Debounce 1s   │    │ • Existing      │    │ • Existing      │      │
    │  │ • .gitignore    │    │ • Pattern match │    │   chunking svc  │    │   backends      │      │
    │  │ • File patterns │    │ • Dependency    │    │ • AST-aware     │    │ • Embeddings    │      │
    │  │ • Recursive     │    │   tracking      │    │ • Smart split   │    │ • Search ready  │      │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘      │
    │           ▲                       ▲                       ▲                       ▲             │
    │           │                       │                       │                       │             │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
    │  │ Service Inject  │    │ Service Inject  │    │ Service Inject  │    │ Service Inject  │      │
    │  │ • ServicesMan   │    │ • Filtering     │    │ • Chunking      │    │ • Backend       │      │
    │  │ • Context prop  │    │   service       │    │   service       │    │   registry      │      │
    │  │ • Health mon    │    │ • Pattern match │    │ • AST parsing   │    │ • Embeddings    │      │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘      │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                 LLM EXPERIENCE                                                 │
    │                                                                                                 │
    │  📍 INDEXING COMPLETELY TRANSPARENT TO LLM USERS                                               │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
    │  │                            SEARCH EXPERIENCE                                            │   │
    │  │                                                                                         │   │
    │  │  LLM: "find authentication functions"                                                  │   │
    │  │   ↓                                                                                     │   │
    │  │  Intent Layer: Processes as SEARCH intent                                              │   │
    │  │   ↓                                                                                     │   │
    │  │  SimpleSearchStrategy: Uses search_code_handler                                        │   │
    │  │   ↓                                                                                     │   │
    │  │  search_code_handler: Searches ALREADY INDEXED content                                 │   │
    │  │   ↓                                                                                     │   │
    │  │  Results: Auth functions found (because indexing happened transparently)              │   │
    │  │                                                                                         │   │
    │  │  🎯 RESULT: LLM gets results without ever knowing indexing occurred                    │   │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
    │  │                           UNDERSTAND EXPERIENCE                                         │   │
    │  │                                                                                         │   │
    │  │  LLM: "understand database architecture"                                               │   │
    │  │   ↓                                                                                     │   │
    │  │  Intent Layer: Processes as UNDERSTAND intent                                          │   │
    │  │   ↓                                                                                     │   │
    │  │  AnalysisWorkflowStrategy: Multi-step analysis                                         │   │
    │  │   ↓                                                                                     │   │
    │  │  Step 1: search_code_handler (uses indexed content)                                    │   │
    │  │  Step 2: ast_grep_search_handler (uses indexed structure)                              │   │
    │  │  Step 3: Summary generation                                                             │   │
    │  │   ↓                                                                                     │   │
    │  │  Results: Comprehensive architecture analysis                                          │   │
    │  │                                                                                         │   │
    │  │  🎯 RESULT: LLM gets rich analysis without manual indexing                             │   │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Service Integration Architecture

```
                    ┌─────────────────────────────────────────────────────────────────┐
                    │                    SERVICES MANAGER                             │
                    │              📍 EXISTING - ENHANCED                            │
                    └─────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              SERVICE REGISTRATION                                               │
    │                                                                                                 │
    │  services_manager.register_service("intent_orchestrator", IntentOrchestrator)                  │
    │  services_manager.register_service("auto_indexing", AutoIndexingService)                       │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
    │  │                            SERVICE DEPENDENCIES                                         │   │
    │  │                                                                                         │   │
    │  │  IntentOrchestrator depends on:          AutoIndexingService depends on:               │   │
    │  │  ├─ caching_service (optional)            ├─ chunking_service (required)               │   │
    │  │  ├─ strategy_registry (internal)          ├─ filtering_service (required)              │   │
    │  │  ├─ parser_factory (internal)             ├─ backend_registry (required)               │   │
    │  │  └─ health_monitoring (inherited)         └─ health_monitoring (inherited)             │   │
    │  │                                                                                         │   │
    │  │  📍 AUTOMATIC DEPENDENCY INJECTION via ServicesManager.get_service_dependency()        │   │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              SERVICE LIFECYCLE                                                  │
    │                                                                                                 │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
    │  │ Service Start   │ ── │ Health Monitor  │ ── │ Operation       │ ── │ Graceful Stop   │      │
    │  │ • Dependency    │    │ • Status check  │    │ • Process       │    │ • Resource      │      │
    │  │   resolution    │    │ • Performance   │    │   requests      │    │   cleanup       │      │
    │  │ • Configuration │    │ • Recovery      │    │ • Health report │    │ • State persist │      │
    │  │ • Initial state │    │ • Alerting      │    │ • Context prop  │    │ • Dependency    │      │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘      │
    │                                                                                                 │
    │  📍 ALL LIFECYCLE MANAGED BY ServicesManager - FOLLOWS EXISTING PATTERNS                       │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              SERVICE CONTEXT CREATION                                           │
    │                                                                                                 │
    │  async def create_intent_context(base_context: dict) -> dict:                                   │
    │      # Uses existing ServicesManager.create_service_context()                                   │
    │      service_context = await services_manager.create_service_context(base_context)             │
    │                                                                                                 │
    │      return {                                                                                   │
    │          **service_context,  # Existing services (chunking, filtering, caching, etc.)         │
    │          "intent_orchestrator": services_manager.get_service("intent_orchestrator"),           │
    │          "auto_indexing": services_manager.get_service("auto_indexing"),                       │
    │          "intent_metadata": {                                                                   │
    │              "session_id": generate_session_id(),                                              │
    │              "timestamp": datetime.now(timezone.utc),                                          │
    │              "request_id": generate_request_id()                                               │
    │          }                                                                                      │
    │      }                                                                                          │
    │                                                                                                 │
    │  📍 ENHANCES EXISTING create_service_context() - NO BREAKING CHANGES                           │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Configuration Integration Architecture

```
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              EXISTING CONFIGURATION HIERARCHY                                   │
    │                                                                                                 │
    │  src/codeweaver/config.py:                                                                     │
    │                                                                                                 │
    │  class CodeWeaverConfig(BaseModel):                                                            │
    │      providers: ProvidersConfig = ProvidersConfig()                                            │
    │      backends: BackendsConfig = BackendsConfig()                                               │
    │      sources: SourcesConfig = SourcesConfig()                                                  │
    │      services: ServicesConfig = ServicesConfig()     # 📍 ENHANCED                            │
    │                                                                                                 │
    │  class ServicesConfig(BaseModel):                                                              │
    │      chunking: ChunkingServiceConfig = ChunkingServiceConfig()                                 │
    │      filtering: FilteringServiceConfig = FilteringServiceConfig()                              │
    │      validation: ValidationServiceConfig = ValidationServiceConfig()                           │
    │      intent: IntentServiceConfig = IntentServiceConfig()           # 📍 NEW                   │
    │      auto_indexing: AutoIndexingConfig = AutoIndexingConfig()      # 📍 NEW                   │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              TOML CONFIGURATION EXAMPLE                                         │
    │                                                                                                 │
    │  # config.toml - EXTENDS EXISTING HIERARCHY                                                    │
    │                                                                                                 │
    │  [services.chunking]                    # Existing service                                      │
    │  max_chunk_size = 1500                                                                          │
    │  min_chunk_size = 50                                                                            │
    │  enabled = true                                                                                 │
    │                                                                                                 │
    │  [services.filtering]                   # Existing service                                      │
    │  max_file_size = 1048576                                                                        │
    │  ignore_patterns = [".git", "node_modules"]                                                     │
    │  enabled = true                                                                                 │
    │                                                                                                 │
    │  [services.intent]                      # 📍 NEW SERVICE                                       │
    │  enabled = true                                                                                 │
    │  default_strategy = "adaptive"                                                                  │
    │  confidence_threshold = 0.6                                                                     │
    │  max_execution_time = 30.0                                                                      │
    │  debug_mode = false                                                                             │
    │  cache_ttl = 3600                                                                               │
    │                                                                                                 │
    │  [services.auto_indexing]               # 📍 NEW SERVICE                                       │
    │  enabled = true                                                                                 │
    │  watch_patterns = ["**/*.py", "**/*.js", "**/*.ts"]                                            │
    │  ignore_patterns = [".git", "node_modules", "__pycache__"]                                     │
    │  debounce_delay = 1.0                                                                           │
    │                                                                                                 │
    │  📍 NO CONFLICTS - EXTENDS EXISTING HIERARCHY CLEANLY                                          │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 FastMCP Middleware Integration Architecture

```
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              EXISTING FASTMCP PIPELINE                                          │
    │                                                                                                 │
    │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
    │  │   Request   │→  │  Chunking   │→  │  Filtering  │→  │   Tools     │→  │  Response   │       │
    │  │ Processing  │   │ Middleware  │   │ Middleware  │   │  Execution  │   │ Generation  │       │
    │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘       │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │  📍 ENHANCED - NOT REPLACED
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              ENHANCED FASTMCP PIPELINE                                          │
    │                                                                                                 │
    │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
    │  │   Request   │→  │   Intent    │→  │   Existing  │→  │   Tool      │→  │  Response   │       │
    │  │ Processing  │   │  Routing    │   │ Middleware  │   │ Execution   │   │ Generation  │       │
    │  │ (existing)  │   │ 📍 NEW      │   │ Pipeline    │   │ (enhanced)  │   │ (existing)  │       │
    │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘       │
    │          │                  │                 │                 │                  │            │
    │          ▼                  ▼                 ▼                 ▼                  ▼            │
    │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
    │  │ Existing    │   │ Intent      │   │ Existing    │   │ Enhanced    │   │ Existing    │       │
    │  │ Request     │   │ Service     │   │ Services    │   │ with Intent │   │ Response    │       │
    │  │ Processing  │   │ Bridge      │   │ Context     │   │ Context     │   │ Formatting  │       │
    │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘       │
    │                                                                                                 │
    │  📍 ADDITIVE ENHANCEMENT - NO BREAKING CHANGES TO EXISTING PIPELINE                            │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              INTENT ROUTING LOGIC                                               │
    │                                                                                                 │
    │  class IntentServiceBridge(ServiceBridge):  # 📍 EXTENDS EXISTING ServiceBridge                │
    │                                                                                                 │
    │      async def route_request(self, request, call_next):                                         │
    │          if request.method == "process_intent":                                                 │
    │              # Route through intent layer                                                       │
    │              context = await self.create_intent_context(request.context)                       │
    │              return await self.intent_orchestrator.process_intent(                             │
    │                  request.params["intent"], context                                             │
    │              )                                                                                  │
    │          else:                                                                                  │
    │              # Pass through to existing tools - NO CHANGES                                     │
    │              return await call_next(request)                                                    │
    │                                                                                                 │
    │  📍 PRESERVES ALL EXISTING TOOL FUNCTIONALITY                                                  │
    │  📍 ADDS INTENT PROCESSING WITHOUT BREAKING CHANGES                                            │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Success Metrics Dashboard (Architecture-Compliant)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                SUCCESS METRICS TRACKING                                         │
│                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          ARCHITECTURAL COMPLIANCE                                       │   │
│  │                                                                                         │   │
│  │  Service Integration:               Configuration Integration:                          │   │
│  │  ├─ BaseServiceProvider: 100% ✅    ├─ ServicesConfig extension: ✅                   │   │
│  │  ├─ ServicesManager usage: 100% ✅  ├─ TOML hierarchy respect: ✅                     │   │
│  │  ├─ Health monitoring: 100% ✅      ├─ Environment overrides: ✅                      │   │
│  │  └─ Context injection: 100% ✅      └─ No conflicts: ✅                               │   │
│  │                                                                                         │   │
│  │  Factory Integration:               FastMCP Integration:                               │   │
│  │  ├─ ExtensibilityManager: 100% ✅   ├─ ServiceBridge pattern: ✅                      │   │
│  │  ├─ Plugin discovery: 100% ✅       ├─ Middleware compatibility: ✅                   │   │
│  │  ├─ Strategy registration: 100% ✅  ├─ Context propagation: ✅                        │   │
│  │  └─ Performance tracking: 100% ✅   └─ No breaking changes: ✅                        │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                │                                                │
│                                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          BACKGROUND INDEXING SUCCESS                                    │   │
│  │                                                                                         │   │
│  │  Auto-Indexing Service:             LLM User Experience:                               │   │
│  │  ├─ Background operation: 100% ✅    ├─ No INDEX intent: ✅                            │   │
│  │  ├─ File watching active: ✅         ├─ Transparent indexing: ✅                       │   │
│  │  ├─ Health monitoring: ✅            ├─ Search always works: ✅                        │   │
│  │  └─ Developer control only: ✅       └─ No manual indexing: ✅                         │   │
│  │                                                                                         │   │
│  │  Service Dependencies:               Framework Developer Control:                      │   │
│  │  ├─ Chunking service: ✅             ├─ start_monitoring(): ✅                         │   │
│  │  ├─ Filtering service: ✅            ├─ stop_monitoring(): ✅                          │   │
│  │  ├─ Backend registry: ✅             ├─ health_check(): ✅                             │   │
│  │  └─ Health monitoring: ✅            └─ Performance metrics: ✅                        │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                │                                                │
│                                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            INTENT PROCESSING ACCURACY                                   │   │
│  │                                                                                         │   │
│  │  Pattern Recognition (NO INDEX):    Service Context Integration:                       │   │
│  │  ├─ SEARCH intent: 95% ✅            ├─ Service injection: 100% ✅                     │   │
│  │  ├─ UNDERSTAND intent: 92% ✅        ├─ Context propagation: 100% ✅                   │   │
│  │  ├─ ANALYZE intent: 90% ✅           ├─ Health monitoring: 100% ✅                     │   │
│  │  └─ NO INDEX intent: N/A ✅          └─ Error recovery: >85% ✅                        │   │
│  │                                                                                         │   │
│  │  Strategy Selection:                 Tool Integration:                                  │   │
│  │  ├─ Correct routing: >95% ✅         ├─ search_code_handler: ✅                        │   │
│  │  ├─ Performance tracking: ✅         ├─ ast_grep_search_handler: ✅                    │   │
│  │  ├─ Service compliance: 100% ✅      ├─ get_supported_languages: ✅                    │   │
│  │  └─ Factory integration: 100% ✅     └─ NO index_codebase_handler: ✅                  │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                │                                                │
│                                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              USER EXPERIENCE METRICS                                    │   │
│  │                                                                                         │   │
│  │  LLM Interface Simplification:       Developer Experience:                             │   │
│  │  ├─ Tools reduced: 4 → 2 ✅          ├─ Zero breaking changes: ✅                      │   │
│  │  ├─ Natural language: 100% ✅        ├─ Existing patterns: 100% ✅                     │   │
│  │  ├─ Context awareness: ✅            ├─ Configuration control: ✅                      │   │
│  │  └─ Background indexing: ✅          └─ Service extensibility: ✅                      │   │
│  │                                                                                         │   │
│  │  Query Success (No INDEX):           System Integration:                               │   │
│  │  ├─ SEARCH queries: >90% ✅          ├─ Services layer: 100% ✅                        │   │
│  │  ├─ UNDERSTAND queries: >85% ✅      ├─ Middleware layer: 100% ✅                      │   │
│  │  ├─ ANALYZE queries: >80% ✅         ├─ Factory layer: 100% ✅                         │   │
│  │  └─ First attempt success: >80% ✅   └─ Implementation layer: 100% ✅                  │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This corrected implementation diagram shows the intent layer properly integrated with CodeWeaver's existing architecture, with the critical fix of removing the INDEX intent from LLM users and implementing it as a transparent background service. All components follow established patterns and maintain architectural compliance while delivering the transformative user experience.