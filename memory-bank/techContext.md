# Technical Context

## Technologies Used

### Programming Language
- Python 3.x

### Key Libraries
- pandas: Data manipulation and CSV file reading
- numpy: Numerical computations
- requests: HTTP requests to Perplexity AI API
- locale: Number formatting according to Brazilian standards
- json: JSON data handling

## Development Setup

### Package Structure
The project is now set up as a proper Python package:
- Installable via pip: `pip install -e .`
- Organized modules in src/ directory
- Package configuration in setup.py

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
        'requests'
    ]
)
```

### Data Sources
1. Census Data Files (Location: D:\jornalera-marista\censo-2022\dados\estados\)
   - Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv
   - compilado_estados.csv

### API Integration
- Service: Perplexity AI
- API Key: Configured in code
- Endpoints Used:
  - /chat/completions

### Project Organization
```
src/
├── data/       # Data processing modules
├── utils/      # Utility functions
├── paragraphs/ # Article generation
└── main.py     # Main execution
```

## Technical Constraints

### API Configuration
- Model: sonar
- Temperature: 0.2 (low for consistent outputs)
- Max Tokens: Varies by query
  - State creation date: 123 tokens
  - Historical info: 500 tokens

### Locale Settings
- Uses pt_BR.UTF-8 for Brazilian number formatting
- Fallback formatting if locale unavailable

## Dependencies
```python
import pandas as pd
import numpy as np
import requests
import json
import locale
```

## Environment Requirements
- Python environment with above packages installed
- Access to Perplexity AI API
- Brazilian locale support (pt_BR.UTF-8)
