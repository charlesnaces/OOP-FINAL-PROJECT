# Architecture Diagram - 3 Core Modules

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         JSONFile                                 │
│              (Smart Orchestrator with Exception Handling)        │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├─────────────────────────┬──────────────────────────┐
             │                         │                          │
             ▼                         ▼                          ▼
    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
    │    Processor     │    │    Analyzer      │    │   Normalizer     │
    │  (Load + Clean)  │    │   (Analyze)      │    │ (Unstructured)   │
    │                  │    │                  │    │                  │
    │ • _load()        │    │ • head()         │    │ • detect()       │
    │ • trim()         │    │ • tail()         │    │ • normalize()    │
    │ • drop_null()    │    │ • stats()        │    │ • display()      │
    │ • drop_dups()    │    │ • filter()       │    │                  │
    │ • clean()        │    │ • to_csv()       │    │ Formats:         │
    │                  │    │ • to_json()      │    │ • COCO           │
    │ 225 lines        │    │                  │    │ • nested_dict    │
    │                  │    │ 174 lines        │    │ • nested_list    │
    └──────────────────┘    └──────────────────┘    │ • array          │
                                                     │                  │
                                                     │ 244 lines        │
                                                     └──────────────────┘
```

## Exception Handling Flow in JSONFile

```
read_json('file.json')
        │
        ▼
   ┌─────────────────────────────────────┐
   │   Try: Processor (load + clean)     │
   └─────────────────────────────────────┘
        │
        ├─ SUCCESS ─────────────────────────────────────────┐
        │                                                   │
        │                    ▼                              │
        │            ┌───────────────────┐                  │
        │            │   Analyzer        │                  │
        │            │ (Analyze + Export)│                  │
        │            └───────────────────┘                  │
        │                    │                              │
        │                    ▼                              │
        └────────────────► JSONFile Ready ◄────────────────┘
                         (return to user)
        
        │
        ├─ InvalidRootError ──────────────────────────────┐
        │ (JSON not a list)                              │
        │                                                │
        │           ▼                                    │
        │    ┌──────────────────────┐                   │
        │    │ Try: Normalizer      │                   │
        │    │ (detect + transform) │                   │
        │    └──────────────────────┘                   │
        │           │                                   │
        │           ▼                                   │
        │    ┌──────────────────────┐                   │
        │    │ Processor (clean)    │                   │
        │    │ (now on structured)  │                   │
        │    └──────────────────────┘                   │
        │           │                                   │
        │           ▼                                   │
        │    ┌──────────────────────┐                   │
        │    │ Analyzer             │                   │
        │    └──────────────────────┘                   │
        │           │                                   │
        └──────────► JSONFile Ready ◄──────────────────┘
                  (return to user)
        
        │
        └─ Other Errors ──► Raise with helpful message
          (FileNotFound, MalformedJSON)
```

## Data Flow

```
         Input File
             │
             ▼
    ┌────────────────┐
    │  Processor     │
    │  • Load JSON   │
    │  • Validate    │
    │  • Clean       │
    └────────────────┘
             │
             ▼
      Cleaned Data
             │
             ▼
    ┌────────────────┐
    │  Analyzer      │
    │  • Statistics  │
    │  • Filter      │
    │  • Export      │
    └────────────────┘
             │
             ▼
        Output Data
    (CSV, JSON, etc)

Optional path if needed:
    Input File (unstructured)
             │
             ▼
    ┌────────────────┐
    │  Normalizer    │
    │  • Detect fmt  │
    │  • Transform   │
    └────────────────┘
             │
             ▼
    Structured Data
             │
        (continue above)
```

## Class Composition

```
JSONFile
├── _process()
│   ├─ Create Processor
│   ├─ On InvalidRootError
│   │  └─ Create Normalizer
│   └─ Create Analyzer
├── head()  ──► Analyzer.head()
├── stats() ──► Analyzer.stats()
├── filter()──► Analyzer.filter_by_value()
└── to_csv()──► Analyzer.to_csv()
```

## Module Dependencies

```
Processor (independent)
  │
  └─── uses: JSONLoader (internal)
       uses: Exceptions

Analyzer (independent)
  │
  └─── uses: Collections, CSV, JSON

Normalizer (independent)
  │
  └─── uses: JSON, Copy

JSONFile
  │
  ├─ uses: Processor
  ├─ uses: Analyzer
  ├─ uses: Normalizer
  └─ uses: Exceptions

No circular dependencies ✅
Clean separation of concerns ✅
```

## User Entry Points

```
                    ┌─────────────────────┐
                    │   read_json()       │ (Recommended)
                    │   (in api.py)       │
                    └────────┬────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │    JSONFile         │
                    │  (Auto-handling)    │
                    └────────┬────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │  Pandas-like API    │
                    │  head(), stats(),   │
                    │  filter(), etc.     │
                    └─────────────────────┘


For advanced users:

Processor ──────┐
                │
Analyzer ───────├─── Import directly
                │    and use manually
Normalizer ─────┘
```

## Size Comparison

```
Module          Lines   Purpose
─────────────────────────────────────────────────
Processor       225     Load + Clean
Analyzer        174     Analyze + Export
Normalizer      244     Handle unstructured
JSONFile        ~165    Orchestrate
API             17      Entry point
Exceptions      10      Custom errors
─────────────────────────────────────────────────
Total           ~835    Complete solution

Before refactor:
loader.py       69
cleaner.py      156
analyzer.py     174
normalizer.py   244
jsonfile.py     166
reader.py       166     ← Redundant
advanced.py     105     ← Redundant
api.py          17
exceptions.py   10
─────────────────────────────────────────────────
Total          1107     (with dead code)

Improvement: 272 lines removed (24% reduction) ✅
```
