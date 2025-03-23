# Product Context

## Purpose
This project aims to automatically generate articles about each Brazilian state by combining:
- Population census data from CSV files
- Historical information retrieved via Perplexity AI API
- Health system information with aging population focus
- Additional internet research data

## Problem Solved
- Automates the creation of comprehensive state articles
- Ensures consistent article structure across all states
- Combines statistical data with historical context
- Standardizes source citations and references
- Provides multi-level fallbacks for data availability
- Saves time in research and article generation
- Maintains consistent text style and formatting

## How It Works
1. Reads population data from two CSV files:
   - Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv
   - compilado_estados.csv

2. For each state, generates:
   - Population growth statistics since first census
   - Ranking comparison with other states
   - Historical information about state creation
   - Economic and political context for specific time periods
   - Health system analysis with aging population focus
   - Infrastructure readiness assessment
   - Chronic care capabilities

3. Output formats:
   - Markdown files for each state
   - Future: HTML article generation
   - Consistent structure across all states
   - Standardized text formatting

4. Source handling:
   - Consistent markdown format: [Fonte: Title](URL)
   - Automatic reference cleanup
   - Fallback to generic sources when needed
   - Prioritizes official and recent (2022-2024) sources

## User Experience Goals
- Generate accurate and informative articles
- Maintain consistent writing style
- Include proper source citations in standardized format
- Format numbers according to Brazilian standards
- Present information in a logical flow
- Provide graceful fallbacks for missing information
- Ensure reliable source references
- Focus on aging population preparedness

## Quality Standards
1. Content Quality:
   - Accurate statistical data
   - Verified historical information
   - Recent health system updates
   - Official source citations

2. Formatting Standards:
   - Brazilian number formatting
   - Consistent paragraph spacing
   - Standardized source citations
   - Clear section headers
   - Proper line breaks
   - Consistent verb tenses
   - Standardized punctuation

3. Text Style Standards:
   - Direct and concise language
   - Future tense for projections
   - Consistent terminology
   - Clear transitions between topics
   - Professional tone
   - Objective presentation

4. Data Reliability:
   - Primary sources preferred
   - Multi-stage fallback system
   - Generic alternatives when needed
   - Clear source attribution

5. Information Flow:
   - Historical context first
   - Current situation analysis
   - Future projections
   - Specialized topics (health, education)
   - Logical progression of ideas

6. File Organization:
   - Separate markdown file for each state
   - Consistent file naming convention
   - Standard directory structure
   - Organized asset management
   - Version control friendly
