# Technical Context

## Technologies Used

### Programming Language
- Python 3.x with type hints

### Key Libraries
- pandas: CSV data handling
- numpy: Numerical operations
- requests: Perplexity AI API calls
- locale: Brazilian number formatting

## Development Setup

### Package Structure
The project is organized as a proper Python package:
- Installable via pip: `pip install -e .`
- Main execution through automacao.py
- Modular organization in src/ directory
- Clear separation of concerns

### Dependencies
```python
# setup.py dependencies
setup(
    name="blog-automatcao",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'typing'  # For type hints
    ]
)
```

### Data Sources
1. Census Data Files (Location: D:\jornalera-marista\censo-2022\dados\estados\)
   - Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv
     * Contains state population data
     * Historical census records
     * Regional rankings
     * Peak population years
     * Regional position data
   - compilado_estados.csv
     * Growth rate data
     * State metadata
     * Regional information

2. Graph Files (Location: D:\jornalera-marista\censo-2022\dados\estados\)
   - graphs_pop_2024\[state].png
     * Historical population graphs
   - graficos_populacao_estados_2070\[state].png
     * Population projection graphs
   - populacao_graficos_0_4_anos\estado_[state].png
     * Children aged 0-4 projection graphs

### API Integration
- Service: Perplexity AI
- API Key: Configured in code (to be moved to config)
- Implementation: PerplexityAPI class
- Endpoints:
  - /chat/completions (for all queries)
- Query Types:
  - State creation dates
  - Historical context

### Project Organization
```
blog-automatcao/
├── automacao.py   # Main entry point
├── src/           # Core modules
│   ├── data/      # Data access layer
│   ├── utils/     # Shared utilities
│   └── paragraphs/# Content generators
│       ├── historical/  # Historical sections
│       ├── graphs/     # Graph handling
│       ├── projections/ # Future projections
│       └── fertility/  # Fertility analysis
└── memory-bank/   # Documentation
```

## Technical Constraints

### API Configuration
- Model: sonar
- Temperature: 0.2 (for consistency)
- Max Tokens:
  - Creation date: 123
  - Historical info: 500
- Error handling with retries

### Data Formatting
- Numbers: Brazilian locale (pt_BR.UTF-8)
- Dates: Brazilian format
- Text: UTF-8 encoding
- Markdown: Image links and formatting
- Graph paths: State-specific naming

### Class Patterns
```python
# DataLoader initialization
data_loader = DataLoader(
    ranking_file="path/to/ranking.csv",
    growth_file="path/to/growth.csv"
)

# API client initialization
api_client = PerplexityAPI(api_key="key")

# Formatter initialization
formatter = BrazilianFormatter()
```

## Dependencies
```python
# Core imports
import pandas as pd
import numpy as np
import requests
import locale
from typing import Dict, List, Optional, Tuple, Any

# Project imports
from src.data.loader import DataLoader
from src.utils.api import PerplexityAPI
from src.utils.formatting import BrazilianFormatter
from src.utils.text_utils import (
    get_ranking_description,
    get_creation_description,
    format_historical_info
)
```

## Environment Requirements
- Python 3.x environment
- Perplexity AI API access
- Brazilian locale support (pt_BR.UTF-8)
- CSV data files accessible
- Image files for graphs:
  * Population history
  * Future projections
  * Children demographics

## Technical Roadmap
1. Configuration System
   - Move API keys to config
   - Configure file paths
   - Environment settings
2. Testing Infrastructure
   - Unit tests for each module
   - Integration tests
   - Mock API responses
3. HTML Generation
   - Template system
   - Image embedding
   - Styling support
4. Multi-State Support
   - Parallel processing
   - Progress tracking
   - Error recovery
