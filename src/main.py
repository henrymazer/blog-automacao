from src.data.loader import load_census_data
from src.paragraphs import (
    generate_growth_paragraph,
    generate_ranking_paragraph,
    generate_creation_paragraph,
    generate_historical_paragraph
)

def generate_article(state_code='AC'):
    """Generate a complete article for a given state."""
    # Load data
    df, df_crescimento = load_census_data()
    
    # Generate paragraphs
    paragraphs = []
    
    # First paragraph - Population growth
    growth = generate_growth_paragraph(df, df_crescimento, state_code)
    if growth:
        paragraphs.append(growth)
    
    # Second paragraph - Ranking
    ranking = generate_ranking_paragraph(df, df_crescimento, state_code)
    if ranking:
        paragraphs.append(ranking)
    
    # Third paragraph - State creation
    creation = generate_creation_paragraph(df, state_code)
    if creation:
        paragraphs.append(creation)
    
    # Fourth paragraph - Historical info
    historical = generate_historical_paragraph(df, state_code)
    if historical:
        paragraphs.append(historical)
    
    # Return article text
    return '\n\n'.join(paragraphs)

if __name__ == '__main__':
    article = generate_article()
    print(article)
