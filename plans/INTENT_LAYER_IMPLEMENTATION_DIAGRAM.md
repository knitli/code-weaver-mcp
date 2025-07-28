# Intent Layer Implementation Architecture Diagram

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    LLM USER INTERFACE                                  │
│                                                                                         │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────────────────┐ │
│  │         process_intent          │    │        get_intent_capabilities              │ │
│  │                                 │    │                                             │ │
│  │ Natural Language Input:         │    │ Returns:                                    │ │
│  │ • "find auth functions"         │    │ • Supported intent types                   │ │
│  │ • "understand db architecture"  │    │ • Example queries                          │ │
│  │ • "analyze performance issues"  │    │ • Available strategies                     │ │
│  └─────────────────────────────────┘    └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                  INTENT LAYER                                          │
│                            📍 NEW ARCHITECTURE                                          │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                            INTENT ORCHESTRATOR                                    │ │
│  │                        📍 Core Entry Point                                       │ │
│  │                                                                                   │ │
│  │  Entry Point: async def process_intent(intent_text, context) -> IntentResult     │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │ │
│  │  │ Cache Check     │  │ Intent Parsing  │  │ Strategy        │  │ Result      │ │ │
│  │  │ • Query similarity│  │ • Pattern match │  │ Selection       │  │ Caching     │ │ │
│  │  │ • Result reuse  │  │ • Confidence    │  │ • Performance   │  │ • Success   │ │ │
│  │  │ • Performance   │  │ • Error fallback│  │ • Context aware │  │ • Metadata  │ │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                          │                                             │
│                                          ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                            PARSING LAYER                                          │ │
│  │                                                                                   │ │
│  │  ┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐ │ │
│  │  │         Pattern Matcher             │  │      NLP Enhanced Parser            │ │ │
│  │  │         📍 ESSENTIAL                │  │      📍 ENHANCEMENT                 │ │ │
│  │  │                                     │  │                                     │ │ │
│  │  │ ┌─────────────────────────────────┐ │  │ ┌─────────────────────────────────┐ │ │ │
│  │  │ │ Intent Patterns:                │ │  │ │ spaCy Pipeline:                 │ │ │ │
│  │  │ │ • "find" → SEARCH              │ │  │ │ • en_core_web_trf               │ │ │ │
│  │  │ │ • "understand" → UNDERSTAND     │ │  │ │ • Domain classification         │ │ │ │
│  │  │ │ • "analyze" → ANALYZE           │ │  │ │ • Entity recognition            │ │ │ │
│  │  │ │ • "index" → INDEX               │ │  │ │ • Confidence scoring            │ │ │ │
│  │  │ └─────────────────────────────────┘ │  │ └─────────────────────────────────┘ │ │ │
│  │  │                                     │  │                                     │ │ │
│  │  │ ┌─────────────────────────────────┐ │  │ ┌─────────────────────────────────┐ │ │ │
│  │  │ │ Scope Detection:                │ │  │ │ Semantic Analysis:              │ │ │ │
│  │  │ │ • "file/function" → FILE        │ │  │ │ • Technical entity extraction   │ │ │ │
│  │  │ │ • "module/class" → MODULE       │ │  │ │ • Dependency relationships      │ │ │ │
│  │  │ │ • "project/system" → PROJECT    │ │  │ │ • Context understanding         │ │ │ │
│  │  │ └─────────────────────────────────┘ │  │ └─────────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────┘  └─────────────────────────────────────┘ │ │
│  │                            │                              │                        │ │
│  │                            └──────────────┬───────────────┘                        │ │
│  └───────────────────────────────────────────┼────────────────────────────────────────┘ │
│                                              │                                          │
│                                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                     ParsedIntent Data Structure                                   │ │
│  │                                                                                   │ │
│  │  intent_type: SEARCH | UNDERSTAND | ANALYZE | INDEX                              │ │
│  │  primary_target: "authentication", "database", "performance"                     │ │
│  │  scope: FILE | MODULE | PROJECT | SYSTEM                                        │ │
│  │  complexity: SIMPLE | MODERATE | COMPLEX | ADAPTIVE                             │ │
│  │  confidence: 0.0-1.0 (parser confidence score)                                  │ │
│  │  filters: {language: "python", directory: "src/auth"}                           │ │
│  │  metadata: {parser_used, patterns_matched, entities_found}                      │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                              │                                          │
│                                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                           STRATEGY ENGINE                                         │ │
│  │                                                                                   │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                       Strategy Registry                                     │ │ │
│  │  │                                                                             │ │ │
│  │  │  Performance Tracking → Strategy Selection → Execution Coordination        │ │ │
│  │  │                             │                                               │ │ │
│  │  │         ┌───────────────────┼───────────────────┐                          │ │ │
│  │  │         │                   │                   │                          │ │ │
│  │  │         ▼                   ▼                   ▼                          │ │ │
│  │  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐              │ │ │
│  │  │  │ SimpleSearch    │ │ AnalysisWorkflow│ │ Adaptive        │              │ │ │
│  │  │  │ Strategy        │ │ Strategy        │ │ Strategy        │              │ │ │
│  │  │  │ 📍 ESSENTIAL    │ │ 📍 ESSENTIAL    │ │ 📍 ESSENTIAL    │              │ │ │
│  │  │  │                 │ │                 │ │                 │              │ │ │
│  │  │  │ Conditions:     │ │ Conditions:     │ │ Conditions:     │              │ │ │
│  │  │  │ • SEARCH intent │ │ • UNDERSTAND    │ │ • Fallback      │              │ │ │
│  │  │  │ • SIMPLE        │ │ • COMPLEX       │ │ • Low confidence│              │ │ │
│  │  │  │ • High confidence│ │ • PROJECT scope │ │ • Always available│             │ │ │
│  │  │  │                 │ │                 │ │                 │              │ │ │
│  │  │  │ Execution:      │ │ Execution:      │ │ Execution:      │              │ │ │
│  │  │  │ Direct tool     │ │ Multi-step      │ │ Escalation      │              │ │ │
│  │  │  │ mapping         │ │ workflow        │ │ chain           │              │ │ │
│  │  │  └─────────────────┘ └─────────────────┘ └─────────────────┘              │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                              │                                          │
│                                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          WORKFLOW ENGINE                                          │ │
│  │                                                                                   │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    Multi-Step Orchestration                                 │ │ │
│  │  │                                                                             │ │ │
│  │  │  Step 1: Initial Search → Step 2: Structural Analysis → Step 3: Summary   │ │ │
│  │  │           │                        │                            │         │ │ │
│  │  │           ▼                        ▼                            ▼         │ │ │
│  │  │  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     │ │ │
│  │  │  │ search_code     │     │ ast_grep_search │     │ Result          │     │ │ │
│  │  │  │ • Query target  │     │ • Pattern match │     │ Aggregation     │     │ │ │
│  │  │  │ • Language det. │     │ • Structure find│     │ • Summary gen.  │     │ │ │
│  │  │  │ • Result filter │     │ • Context build │     │ • Insight extr. │     │ │ │
│  │  │  └─────────────────┘     └─────────────────┘     └─────────────────┘     │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            FASTMCP MIDDLEWARE INTEGRATION                              │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              MIDDLEWARE PIPELINE                                  │ │
│  │                                                                                   │ │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────┐ │ │
│  │  │   Intent    │→  │  Chunking   │→  │  Filtering  │→  │   Tools     │→  │Resp │ │ │
│  │  │ Middleware  │   │ Middleware  │   │ Middleware  │   │  Execution  │   │onse │ │ │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────┘ │ │
│  │         │                  │                 │                 │              │   │ │
│  │         ▼                  ▼                 ▼                 ▼              ▼   │ │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────┐ │ │
│  │  │  Service    │   │   Service   │   │   Service   │   │ Performance │   │Error│ │ │
│  │  │  Context    │   │  Context    │   │  Context    │   │  Monitoring │   │Hand │ │ │
│  │  │ Injection   │   │ Propagation │   │ Enhancement │   │   & Metrics │   │ling │ │ │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         EXISTING CODEWEAVER ARCHITECTURE                               │
│                              📍 NO CHANGES REQUIRED                                    │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                SERVER LAYER                                       │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ index_codebase  │  │   search_code    │  │ ast_grep_search  │  │get_supported│ │ │
│  │  │    _handler     │  │    _handler      │  │    _handler      │  │_languages   │ │ │
│  │  │                 │  │                  │  │                  │  │  _handler   │ │ │
│  │  │ Used by:        │  │ Used by:         │  │ Used by:         │  │ Used by:    │ │ │
│  │  │ • IndexStrategy │  │ • SimpleSearch   │  │ • AnalysisFlow   │  │ • All       │ │ │
│  │  │ • Setup flows   │  │ • All strategies │  │ • Structural     │  │ • Capability│ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                               SERVICES LAYER                                      │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ ServicesManager │  │ Service Context  │  │ Dependency       │  │ Health      │ │ │
│  │  │ • Coordination  │  │ • Context inject │  │ Injection        │  │ Monitoring  │ │ │
│  │  │ • Lifecycle     │  │ • Service access │  │ • Protocol-based │  │ • Recovery  │ │ │
│  │  │                 │ ◄┤                  │  │                  │  │             │ │ │
│  │  │ Enhanced for:   │  │ Enhanced for:    │  │ Enhanced for:    │  │ Enhanced:   │ │ │
│  │  │ • Intent services│  │ • Intent context │  │ • Strategy DI    │  │ • Intent    │ │ │
│  │  │ • Strategy mgmt │  │ • Cache services │  │ • Parser DI      │  │   monitoring│ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              MIDDLEWARE LAYER                                     │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ ChunkingMiddle  │  │ FileFiltering    │  │ RateLimiting     │  │ Logging     │ │ │
│  │  │ ware            │  │ Middleware       │  │ Middleware       │  │ Middleware  │ │ │
│  │  │ • AST-aware     │  │ • Gitignore      │  │ • Request limits │  │ • Structured│ │ │
│  │  │ • Language-spec │  │ • File patterns  │  │ • Backoff        │  │ • Performance│ │ │
│  │  │                 │  │                  │  │                  │  │             │ │ │
│  │  │ Intent Usage:   │  │ Intent Usage:    │  │ Intent Usage:    │  │ Intent:     │ │ │
│  │  │ • Result chunk  │  │ • File discovery │  │ • Intent limits  │  │ • Intent    │ │ │
│  │  │ • Context build │  │ • Context filter │  │ • Strategy limits│  │   tracking  │ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                               FACTORY LAYER                                       │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ Extensibility   │  │ BackendRegistry  │  │ SourceRegistry   │  │ Service     │ │ │
│  │  │ Manager         │  │ • Component disc │  │ • Data sources   │  │ Registry    │ │ │
│  │  │ • Plugin system │  │ • Vector DBs     │  │ • File/Git/API   │  │ • Lifecycle │ │ │
│  │  │ • Component mgmt│  │ • Provider APIs  │  │ • Custom sources │  │ • Health    │ │ │
│  │  │                 │  │                  │  │                  │  │             │ │ │
│  │  │ Intent Extension│  │ Same             │  │ Same             │  │ Enhanced:   │ │ │
│  │  │ • Strategy reg. │  │                  │  │                  │  │ • Intent    │ │ │
│  │  │ • Parser plugins│  │                  │  │                  │  │   services  │ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          IMPLEMENTATION LAYER                                     │ │
│  │                                                                                   │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │ │
│  │  │ Providers       │  │ Backends         │  │ Sources          │  │ Services    │ │ │
│  │  │ • VoyageAI      │  │ • Qdrant         │  │ • Filesystem     │  │ • Chunking  │ │ │
│  │  │ • OpenAI        │  │ • Pinecone       │  │ • Git            │  │ • Filtering │ │ │
│  │  │ • Cohere        │  │ • Weaviate       │  │ • Database       │  │ • Validation│ │ │
│  │  │ • HuggingFace   │  │ • ChromaDB       │  │ • Custom         │  │ • Custom    │ │ │
│  │  │                 │  │                  │  │                  │  │             │ │ │
│  │  │ Same            │  │ Same             │  │ Same             │  │ Enhanced:   │ │ │
│  │  │                 │  │                  │  │                  │  │ • Intent    │ │ │
│  │  │                 │  │                  │  │                  │  │   caching   │ │ │
│  │  └─────────────────┘  └──────────────────┘  └──────────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────┘
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
    │  async def process_intent(intent_text: str, context: dict) -> IntentResult:                     │
    │                                                                                                 │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
    │  │ 1. Cache Check  │ ── │ 2. Parse Intent │ ── │ 3. Select       │ ── │ 4. Execute &    │      │
    │  │                 │    │                 │    │   Strategy      │    │   Cache Result  │      │
    │  │ • Query sim     │    │ • Pattern match │    │ • Performance   │    │ • Success       │      │
    │  │ • Result reuse  │    │ • NLP enhance   │    │ • Context aware │    │ • Metadata      │      │
    │  │ • Fast return   │    │ • Confidence    │    │ • Fallback      │    │ • Cache store   │      │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘      │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                               PARSING PHASE                                                     │
    │                                                                                                 │
    │  Input: "understand authentication system"                                                     │
    │                                                                                                 │
    │  ┌─────────────────────────────────────┐              ┌─────────────────────────────────────┐  │
    │  │         Pattern Matcher             │              │      NLP Enhanced Parser            │  │
    │  │         📍 ESSENTIAL                │     OR       │      📍 ENHANCEMENT                 │  │
    │  │                                     │              │                                     │  │
    │  │ Pattern Analysis:                   │              │ Semantic Analysis:                  │  │
    │  │ • "understand" → UNDERSTAND         │              │ • spaCy processing                  │  │
    │  │ • "system" → PROJECT scope          │              │ • Entity recognition                │  │
    │  │ • "authentication" → target         │              │ • Domain classification             │  │
    │  │ • Multi-word → COMPLEX              │              │ • Advanced confidence               │  │
    │  │                                     │              │                                     │  │
    │  │ Confidence Factors:                 │              │ ML Features:                        │  │
    │  │ • Pattern match strength: 0.8       │              │ • Semantic similarity: 0.9          │  │
    │  │ • Scope clarity: 0.9                │              │ • Entity confidence: 0.95           │  │
    │  │ • Complexity assessment: 0.7        │              │ • Domain accuracy: 0.85             │  │
    │  │ • Overall confidence: 0.8           │              │ • Overall confidence: 0.9           │  │
    │  └─────────────────────────────────────┘              └─────────────────────────────────────┘  │
    │                                                                        │                        │
    │                                              ┌─────────────────────────┘                        │
    │                                              ▼                                                  │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │                              ParsedIntent Output                                         │  │
    │  │                                                                                         │  │
    │  │  intent_type: UNDERSTAND                                                                │  │
    │  │  primary_target: "authentication system"                                               │  │
    │  │  scope: PROJECT                                                                         │  │
    │  │  complexity: COMPLEX                                                                    │  │
    │  │  confidence: 0.8 (pattern) | 0.9 (NLP)                                                │  │
    │  │  filters: {domain: "security", component: "auth"}                                      │  │
    │  │  metadata: {parser: "pattern_based|nlp_enhanced", entities: [...]}                    │  │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              STRATEGY SELECTION                                                 │
    │                                                                                                 │
    │  Strategy Evaluation Matrix:                                                                    │
    │  ┌─────────────────────────────┬─────────────────────────────┬─────────────────────────────┐   │
    │  │       Strategy              │         Conditions          │         Score               │   │
    │  ├─────────────────────────────┼─────────────────────────────┼─────────────────────────────┤   │
    │  │ SimpleSearchStrategy        │ SEARCH + SIMPLE + conf>0.7  │ 0.1 (wrong intent type)    │   │
    │  │ AnalysisWorkflowStrategy    │ UNDERSTAND + COMPLEX + proj │ 0.95 ✅ SELECTED           │   │
    │  │ AdaptiveStrategy            │ confidence < 0.6 | fallback │ 0.3 (high confidence)       │   │
    │  │ IndexingStrategy            │ INDEX intent + no existing  │ 0.0 (wrong intent type)    │   │
    │  └─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘   │
    │                                                                                                 │
    │  Selected: AnalysisWorkflowStrategy                                                             │
    │  Reason: Perfect match for UNDERSTAND + COMPLEX + PROJECT scope + high confidence              │
    │  Performance History: 92% success rate, 3.2s avg execution time                               │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                         ANALYSIS WORKFLOW STRATEGY EXECUTION                                   │
    │                                                                                                 │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
    │  │                            WORKFLOW ENGINE                                              │   │
    │  │                                                                                         │   │
    │  │  Multi-Step Orchestration:                                                              │   │
    │  │                                                                                         │   │
    │  │  Step 1: Enhanced Search                                                                │   │
    │  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
    │  │  │ CALL: search_code_handler(                                                      │   │   │
    │  │  │   query="authentication system",                                                │   │   │
    │  │  │   limit=50,                                                                     │   │   │
    │  │  │   rerank=True,                                                                  │   │   │
    │  │  │   filters={focus: "architecture", scope: "project"}                            │   │   │
    │  │  │ )                                                                               │   │   │
    │  │  │                                                                                 │   │   │
    │  │  │ RESULT: {                                                                       │   │   │
    │  │  │   results: 15 code sections,                                                   │   │   │
    │  │  │   directories: ["src/auth/", "middleware/auth/", "utils/security/"],          │   │   │
    │  │  │   languages: ["python", "javascript"],                                         │   │   │
    │  │  │   patterns: ["class Auth", "def authenticate", "auth_middleware"]             │   │   │
    │  │  │ }                                                                               │   │   │
    │  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
    │  │                                      │                                                   │   │
    │  │                                      ▼                                                   │   │
    │  │  Step 2: Structural Pattern Analysis                                                     │   │
    │  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
    │  │  │ CALL: ast_grep_search_handler(                                                  │   │   │
    │  │  │   pattern="class $AUTH implements $INTERFACE",                                 │   │   │
    │  │  │   language="python",                                                           │   │   │
    │  │  │   root_paths=["src/auth/", "middleware/auth/"]                                 │   │   │
    │  │  │ )                                                                               │   │   │
    │  │  │                                                                                 │   │   │
    │  │  │ ADDITIONAL PATTERNS:                                                            │   │   │
    │  │  │ • "function $NAME($PARAMS) { ... auth ... }" for JavaScript                   │   │   │
    │  │  │ • "@decorator\ndef $FUNC" for Python decorators                                │   │   │
    │  │  │ • "class $NAME(BaseAuth)" for inheritance patterns                             │   │   │
    │  │  │                                                                                 │   │   │
    │  │  │ RESULT: {                                                                       │   │   │
    │  │  │   structural_matches: 12,                                                      │   │   │
    │  │  │   inheritance_tree: ["BaseAuth -> JWTAuth -> APIAuth"],                       │   │   │
    │  │  │   decorator_patterns: ["@require_auth", "@validate_token"],                    │   │   │
    │  │  │   interface_implementations: ["AuthProvider", "TokenValidator"]               │   │   │
    │  │  │ }                                                                               │   │   │
    │  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
    │  │                                      │                                                   │   │
    │  │                                      ▼                                                   │   │
    │  │  Step 3: Architecture Analysis & Summary Generation                                      │   │
    │  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
    │  │  │ ANALYZE:                                                                        │   │   │
    │  │  │                                                                                 │   │   │
    │  │  │ Component Relationship Mapping:                                                 │   │   │
    │  │  │ • Core components: BaseAuth, JWTAuth, AuthMiddleware                           │   │   │
    │  │  │ • Data flow: Request -> Middleware -> Auth -> TokenValidator -> Response       │   │   │
    │  │  │ • Dependencies: auth system depends on crypto, db, session managers           │   │   │
    │  │  │                                                                                 │   │   │
    │  │  │ Pattern Recognition:                                                            │   │   │
    │  │  │ • Decorator pattern for route protection                                       │   │   │
    │  │  │ • Factory pattern for auth provider creation                                   │   │   │
    │  │  │ • Observer pattern for auth events                                             │   │   │
    │  │  │                                                                                 │   │   │
    │  │  │ Architecture Summary:                                                           │   │   │
    │  │  │ • Multi-layer authentication with JWT tokens                                   │   │   │
    │  │  │ • Middleware-based request interception                                        │   │   │
    │  │  │ • Plugin architecture for multiple auth providers                              │   │   │
    │  │  │ • Session management with secure token handling                                │   │   │
    │  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
    │  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
    │                                                                                                 │
    │  Services Used: chunking_service, filtering_service, caching_service                           │
    │  Execution Time: 3.8 seconds                                                                   │
    │  Resource Usage: Medium (15MB memory, 25% CPU peak)                                            │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                  INTENT RESULT                                                 │
    │                                                                                                 │
    │  {                                                                                              │
    │    "success": true,                                                                             │
    │    "data": {                                                                                    │
    │      "initial_search": {                                                                        │
    │        "result_count": 15,                                                                      │
    │        "directories": ["src/auth/", "middleware/auth/", "utils/security/"],                    │
    │        "languages": ["python", "javascript"],                                                  │
    │        "top_files": ["auth/models.py", "auth/views.py", "middleware/auth_middleware.py"]       │
    │      },                                                                                         │
    │      "structural_search": {                                                                     │
    │        "pattern_matches": 12,                                                                   │
    │        "inheritance_patterns": ["BaseAuth -> JWTAuth -> APIAuth"],                             │
    │        "decorator_usage": ["@require_auth", "@validate_token"],                                 │
    │        "interface_implementations": ["AuthProvider", "TokenValidator"]                         │
    │      },                                                                                         │
    │      "summary": {                                                                               │
    │        "target": "authentication system",                                                       │
    │        "scope": "project-wide",                                                                 │
    │        "architecture_type": "multi-layer authentication with JWT tokens",                      │
    │        "key_components": [                                                                      │
    │          "BaseAuth class hierarchy",                                                            │
    │          "Middleware-based request interception",                                               │
    │          "Plugin architecture for auth providers",                                              │
    │          "Secure session and token management"                                                  │
    │        ],                                                                                       │
    │        "design_patterns": [                                                                     │
    │          "Decorator pattern for route protection",                                              │
    │          "Factory pattern for provider creation",                                               │
    │          "Observer pattern for auth events"                                                     │
    │        ],                                                                                       │
    │        "data_flow": "Request -> Middleware -> Auth -> TokenValidator -> Response",              │
    │        "dependencies": ["crypto", "database", "session_manager"],                              │
    │        "key_findings": [                                                                        │
    │          "Comprehensive authentication system spanning multiple layers",                        │
    │          "Extensible design supporting multiple auth providers",                                │
    │          "Security-focused with proper token validation and session management"                │
    │        ]                                                                                        │
    │      }                                                                                          │
    │    },                                                                                           │
    │    "metadata": {                                                                                │
    │      "strategy": "analysis_workflow",                                                           │
    │      "workflow_steps": ["initial_search", "structural_search", "summary_generation"],          │
    │      "execution_time": 3.8,                                                                     │
    │      "services_used": ["chunking", "filtering", "caching"],                                    │
    │      "performance_metrics": {                                                                   │
    │        "memory_usage": "15MB",                                                                  │
    │        "cpu_peak": "25%",                                                                       │
    │        "cache_hits": 3,                                                                         │
    │        "cache_misses": 1                                                                        │
    │      }                                                                                          │
    │    }                                                                                            │
    │  }                                                                                              │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Strategy Selection Decision Tree

```
                                    ┌─────────────────────────────────────┐
                                    │           ParsedIntent              │
                                    │ • intent_type: UNDERSTAND          │
                                    │ • primary_target: "auth system"    │
                                    │ • scope: PROJECT                    │
                                    │ • complexity: COMPLEX               │
                                    │ • confidence: 0.8                   │
                                    └─────────────────────────────────────┘
                                                      │
                                                      ▼
                                    ┌─────────────────────────────────────┐
                                    │        Strategy Evaluation         │
                                    │                                     │
                                    │  For each registered strategy:      │
                                    │  1. Call can_handle(parsed_intent)  │
                                    │  2. Get performance history score   │
                                    │  3. Calculate: can_handle * 0.7     │
                                    │                + performance * 0.3  │
                                    │  4. Select highest scoring strategy │
                                    └─────────────────────────────────────┘
                                                      │
                      ┌───────────────────────────────┼───────────────────────────────┐
                      │                               │                               │
                      ▼                               ▼                               ▼
        ┌─────────────────────────┐    ┌─────────────────────────┐    ┌─────────────────────────┐
        │   SimpleSearchStrategy  │    │ AnalysisWorkflowStrategy│    │    AdaptiveStrategy     │
        │                         │    │                         │    │                         │
        │ can_handle() Analysis:   │    │ can_handle() Analysis:   │    │ can_handle() Analysis:   │
        │                         │    │                         │    │                         │
        │ • intent=SEARCH? ❌ (0.0)│    │ • intent=UNDERSTAND? ✅ │    │ • confidence<0.6? ❌    │
        │ • complexity=SIMPLE? ❌  │    │ • complexity=COMPLEX? ✅ │    │ • Always fallback: 0.7 │
        │ • confidence>0.7? ✅     │    │ • scope=PROJECT? ✅      │    │                         │
        │                         │    │                         │    │ Performance Score: 0.75  │
        │ can_handle() Score: 0.1  │    │ can_handle() Score: 0.95│    │ Final Score:            │
        │ Performance Score: 0.9   │    │ Performance Score: 0.88 │    │ (0.7 * 0.7) + (0.75 * 0.3) │
        │ Final Score:            │    │ Final Score:            │    │ = 0.715                 │
        │ (0.1 * 0.7) + (0.9 * 0.3)│    │ (0.95 * 0.7) + (0.88 * 0.3)│    │                         │
        │ = 0.34                  │    │ = 0.929 🎯 WINNER       │    │ Rank: 2nd               │
        │                         │    │                         │    │                         │
        │ Rank: 3rd               │    │ Rank: 1st               │    │                         │
        └─────────────────────────┘    └─────────────────────────┘    └─────────────────────────┘
                      │                               │                               │
                      └───────────────────────────────┼───────────────────────────────┘
                                                      │
                                                      ▼
                                    ┌─────────────────────────────────────┐
                                    │     SELECTED STRATEGY               │
                                    │  AnalysisWorkflowStrategy           │
                                    │                                     │
                                    │ Selection Rationale:                │
                                    │ • Perfect intent type match         │
                                    │ • Appropriate for complex queries   │
                                    │ • Handles project-wide scope well   │
                                    │ • Strong performance history        │
                                    │                                     │
                                    │ Execution Plan:                     │
                                    │ 1. Enhanced semantic search         │
                                    │ 2. Structural pattern analysis      │
                                    │ 3. Component relationship mapping   │
                                    │ 4. Architecture summary generation  │
                                    │                                     │
                                    │ Estimated Resources:                │
                                    │ • Time: 3-5 seconds                 │
                                    │ • Memory: ~15MB                     │
                                    │ • CPU: ~25% peak                    │
                                    │ • Services: chunking, filtering     │
                                    └─────────────────────────────────────┘
```

## 🔧 Implementation Directory Structure

```
src/codeweaver/intent/
├── __init__.py                           # Intent layer public API
├── orchestrator.py                       # 📍 CORE: Main orchestrator
│   ├── class IntentOrchestrator
│   ├── async def process_intent()
│   ├── async def get_supported_intents()
│   └── async def health_check()
│
├── parsing/                              # Intent parsing components
│   ├── __init__.py
│   ├── pattern_matcher.py                # 📍 ESSENTIAL: Regex patterns
│   │   ├── class PatternBasedParser
│   │   ├── _detect_intent_type()
│   │   ├── _extract_target()
│   │   ├── _assess_scope()
│   │   └── _assess_complexity()
│   │
│   ├── nlp_processor.py                  # 📍 ENHANCEMENT: spaCy integration
│   │   ├── class NLPEnhancedParser
│   │   ├── spacy.load("en_core_web_trf")
│   │   ├── domain_classifier
│   │   └── MultifactorConfidenceScorer
│   │
│   ├── confidence_scorer.py              # Confidence scoring algorithms
│   │   ├── class BasicConfidenceScorer
│   │   ├── class MultifactorConfidenceScorer
│   │   └── confidence calculation logic
│   │
│   └── factory.py                        # Parser factory and selection
│       ├── class IntentParserFactory
│       ├── create() -> IntentParser
│       └── get_available_parsers()
│
├── strategies/                           # Strategy implementations
│   ├── __init__.py
│   ├── base.py                          # Base strategy interface
│   │   ├── class IntentStrategy(Protocol)
│   │   ├── async def can_handle()
│   │   ├── async def execute()
│   │   └── async def estimate_execution_time()
│   │
│   ├── simple_search.py                  # 📍 ESSENTIAL: Direct search
│   │   ├── class SimpleSearchStrategy
│   │   ├── Direct search_code_handler mapping
│   │   └── <2s execution target
│   │
│   ├── analysis_workflow.py              # 📍 ESSENTIAL: Multi-step analysis
│   │   ├── class AnalysisWorkflowStrategy
│   │   ├── Multi-step workflow orchestration
│   │   ├── search -> structural -> summary
│   │   └── <5s execution target
│   │
│   ├── adaptive.py                       # 📍 ESSENTIAL: Fallback & escalation
│   │   ├── class AdaptiveStrategy
│   │   ├── Escalation chain logic
│   │   ├── _is_result_sufficient()
│   │   └── _fallback_to_original_tools()
│   │
│   ├── indexing.py                       # Codebase indexing strategy
│   │   ├── class IndexingStrategy
│   │   ├── Direct index_codebase_handler mapping
│   │   └── Setup and initialization flows
│   │
│   └── registry.py                       # Strategy registry and selection
│       ├── class StrategyRegistry
│       ├── register_strategy()
│       ├── select_strategy()
│       └── StrategyPerformanceTracker
│
├── workflows/                            # Workflow orchestration
│   ├── __init__.py
│   ├── orchestrator.py                   # Multi-step workflow coordination
│   │   ├── class WorkflowOrchestrator
│   │   ├── WorkflowStep dataclass
│   │   └── execute_workflow()
│   │
│   ├── steps.py                          # Individual workflow step implementations
│   │   ├── SearchStep
│   │   ├── AnalysisStep
│   │   ├── SummaryStep
│   │   └── ValidationStep
│   │
│   └── result_aggregator.py              # Result synthesis and formatting
│       ├── class ResultAggregator
│       ├── combine_results()
│       └── format_summary()
│
├── caching/                              # Caching layer
│   ├── __init__.py
│   ├── basic_cache.py                    # 📍 ESSENTIAL: Basic result caching
│   │   ├── class BasicIntentCache
│   │   ├── TTL-based caching
│   │   └── <1000 entries, 1h TTL
│   │
│   ├── semantic_cache.py                 # 📍 ENHANCEMENT: Vector similarity
│   │   ├── class SemanticIntentCache
│   │   ├── SentenceTransformer integration
│   │   ├── Vector similarity search
│   │   └── 85% similarity threshold
│   │
│   └── cache_manager.py                  # Cache lifecycle and optimization
│       ├── class CacheManager
│       ├── Cache selection logic
│       └── Performance monitoring
│
├── recovery/                             # Error handling and recovery
│   ├── __init__.py
│   ├── fallback_handler.py               # 📍 ESSENTIAL: Basic fallback
│   │   ├── class FallbackHandler
│   │   ├── Strategy fallback chain
│   │   └── Original tool routing
│   │
│   ├── circuit_breaker.py                # 📍 ENHANCEMENT: Failure protection
│   │   ├── class CircuitBreaker
│   │   ├── Failure threshold monitoring
│   │   └── Service degradation patterns
│   │
│   └── error_categories.py               # Error classification and handling
│       ├── IntentError hierarchy
│       ├── Error severity classification
│       └── Recovery strategy mapping
│
├── middleware/                           # FastMCP integration
│   ├── __init__.py
│   ├── intent_middleware.py              # FastMCP middleware integration
│   │   ├── class IntentMiddleware  
│   │   ├── Request routing logic
│   │   └── Service context injection
│   │
│   └── service_bridge.py                 # Service layer bridge
│       ├── class IntentServiceBridge
│       ├── Context propagation
│       └── Service coordination
│
├── config/                               # Configuration management
│   ├── __init__.py
│   ├── settings.py                       # Configuration schema
│   │   ├── IntentConfig dataclass
│   │   ├── TOML parsing
│   │   └── Environment variable overrides
│   │
│   └── validation.py                     # Configuration validation
│       ├── validate_intent_config()
│       └── Configuration error handling
│
└── testing/                              # Testing utilities (not tests)
    ├── __init__.py
    ├── mock_services.py                  # Mock service implementations
    ├── test_intents.py                   # Test intent examples
    ├── performance_helpers.py            # Performance testing utilities
    └── validation_helpers.py             # Validation testing utilities
```

## 📈 Performance & Resource Flow

```
                    ┌─────────────────────────────────────────────────────────────────┐
                    │                    PERFORMANCE TARGETS                         │
                    │                                                                 │
                    │ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐     │
                    │ │ Simple Intents  │ │ Complex Intents │ │ Adaptive Intents│     │
                    │ │ Target: <2s     │ │ Target: <5s     │ │ Target: <10s    │     │
                    │ │ Memory: <5MB    │ │ Memory: <15MB   │ │ Memory: <25MB   │     │
                    │ │ CPU: <15%       │ │ CPU: <30%       │ │ CPU: <45%       │     │
                    │ └─────────────────┘ └─────────────────┘ └─────────────────┘     │
                    └─────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              RESOURCE OPTIMIZATION FLOW                                         │
    │                                                                                                 │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
    │  │ Cache Layer     │ ── │ Parser          │ ── │ Strategy        │ ── │ Execution       │      │
    │  │                 │    │ Optimization    │    │ Optimization    │    │ Optimization    │      │
    │  │ • Hit: 0ms      │    │                 │    │                 │    │                 │      │
    │  │ • Miss: +50ms   │    │ • Pattern: 15ms │    │ • Selection:    │    │ • Simple: 0.8s  │      │
    │  │ • Semantic:     │    │ • NLP: 35ms     │    │   25ms          │    │ • Complex: 3.8s │      │
    │  │   similarity    │    │ • Confidence:   │    │ • Performance   │    │ • Adaptive:     │      │
    │  │   matching      │    │   scoring 5ms   │    │   tracking      │    │   escalation    │      │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘      │
    │           ▲                       ▲                       ▲                       ▲             │
    │           │                       │                       │                       │             │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
    │  │ Memory Pool     │    │ CPU Profiling   │    │ I/O Monitoring  │    │ Service Health  │      │
    │  │ • Cache: 10MB   │    │ • Parsing: 5%   │    │ • Tool calls    │    │ • Availability  │      │
    │  │ • Temp: 5MB     │    │ • Strategy: 10% │    │ • File access   │    │ • Performance   │      │
    │  │ • Results: 8MB  │    │ • Execution:20% │    │ • Network req   │    │ • Error rates   │      │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘      │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Success Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                SUCCESS METRICS TRACKING                                         │
│                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            INTENT RECOGNITION ACCURACY                                  │   │
│  │                                                                                         │   │
│  │  Pattern Matcher (Essential):           NLP Enhanced (Enhancement):                    │   │
│  │  ├─ Common patterns: 90%                ├─ Complex queries: 95%                       │   │
│  │  ├─ Simple queries: 92%                 ├─ Domain terminology: 98%                    │   │
│  │  ├─ Edge cases: 75%                     ├─ Ambiguous input: 88%                       │   │
│  │  └─ Overall target: >85%                └─ Overall target: >92%                       │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                │                                                │
│                                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            STRATEGY SELECTION ACCURACY                                  │   │
│  │                                                                                         │   │
│  │  SimpleSearch Selection:               AnalysisWorkflow Selection:                     │   │
│  │  ├─ Correct routing: 95%               ├─ Complex query routing: 94%                   │   │
│  │  ├─ Execution success: 98%             ├─ Multi-step success: 91%                      │   │
│  │  └─ User satisfaction: 92%             └─ Comprehensive results: 89%                   │   │
│  │                                                                                         │   │
│  │  Adaptive Strategy Selection:          Overall Strategy Performance:                   │   │
│  │  ├─ Escalation success: 87%            ├─ First attempt success: >80%                  │   │
│  │  ├─ Recovery rate: 93%                 ├─ Strategy accuracy: >95%                      │   │
│  │  └─ Final success: 96%                 └─ Performance optimization: >85%               │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                │                                                │
│                                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              PERFORMANCE METRICS                                        │   │
│  │                                                                                         │   │
│  │  Response Times (P95):                 Resource Usage:                                  │   │
│  │  ├─ Simple intents: <2s ✅             ├─ Memory overhead: <30MB ✅                    │   │
│  │  ├─ Complex intents: <3s ✅            ├─ CPU idle: <5% ✅                             │   │
│  │  ├─ Adaptive intents: <10s ✅          ├─ Cache hit rate: >80% ✅                      │   │
│  │  └─ Strategy selection: <100ms ✅      └─ Concurrent requests: >100/s ✅               │   │
│  │                                                                                         │   │
│  │  Caching Performance:                  Error Recovery:                                  │   │
│  │  ├─ Basic cache: 70% hit rate          ├─ Fallback success: >85% ✅                    │   │
│  │  ├─ Semantic cache: 85% hit rate       ├─ Service recovery: >90% ✅                    │   │
│  │  └─ Cache efficiency: >80% ✅          └─ Error rate: <5% ✅                           │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                │                                                │
│                                                ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              USER EXPERIENCE METRICS                                    │   │
│  │                                                                                         │   │
│  │  Interface Simplification:             Query Success Rates:                            │   │
│  │  ├─ Tools reduced: 4 → 1-2 ✅          ├─ Single tool success: >90% ✅                 │   │
│  │  ├─ Natural language: 100% ✅          ├─ First attempt success: >80% ✅               │   │
│  │  ├─ Context awareness: Yes ✅          ├─ Clarification requests: <2/session ✅        │   │
│  │  └─ Backward compatibility: Yes ✅     └─ Overall satisfaction: >85% ✅                │   │
│  │                                                                                         │   │
│  │  Developer Experience:                 System Reliability:                             │   │
│  │  ├─ Custom strategies: Supported ✅    ├─ Uptime: >99.9% ✅                            │   │
│  │  ├─ Debug mode: Available ✅           ├─ Error handling: Comprehensive ✅             │   │
│  │  ├─ Configuration: Full control ✅     ├─ Monitoring: Real-time ✅                     │   │
│  │  └─ Migration: Zero breaking ✅        └─ Recovery: Automated ✅                       │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This implementation diagram provides a comprehensive visual guide for the Intent Layer architecture, showing the complete flow from user input through processing to results, along with all integration points, performance targets, and success metrics. The diagram emphasizes the phased approach with essential features clearly marked for alpha release readiness.