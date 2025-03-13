# Product Context

## Purpose
This project aims to automatically generate articles about each Brazilian state by combining:
- Population census data from CSV files
- Historical information retrieved via Perplexity AI API
- Additional internet research data

## Problem Solved
- Automates the creation of comprehensive state articles
- Ensures consistent article structure across all states
- Combines statistical data with historical context
- Saves time in research and article generation

## How It Works
1. Reads population data from two CSV files:
   - Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv
   - compilado_estados.csv

2. For each state, generates:
   - Population growth statistics since first census
   - Ranking comparison with other states
   - Historical information about state creation
   - Economic and political context for specific time periods

3. Output format:
   - Currently: Console output in Portuguese
   - Future: HTML article generation

## User Experience Goals
- Generate accurate and informative articles
- Maintain consistent writing style
- Include proper source citations
- Format numbers according to Brazilian standards
- Present information in a logical flow
