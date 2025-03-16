import pandas as pd
from src.utils.text_utils import get_ranking_description
from src.utils.formatting import BrazilianFormatter

def generate_peak_comparison_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph comparing state's growth with others for the peak period.
    
    Args:
        data_loader: DataLoader instance with census and growth data
        state_code: Two-letter state code (default: 'AC' for Acre)
        
    Returns:
        Formatted paragraph text describing growth ranking
    """
    # Get state info and basic data
    state_info, _, _, total_states = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    region = state_info['region']
    
    # Get peak period data
    df = data_loader.df_growth
    state_data = df[df['Estado'] == state_code]
    if state_data.empty:
        return None
        
    # Find peak growth period
    growth_cols = [col for col in df.columns if col.startswith("Taxa_Crescimento_Geometrico_")]
    max_rate = float('-inf')
    peak_column = None
    
    for col in growth_cols:
        rate = state_data[col].iloc[0]
        if pd.notna(rate) and rate > max_rate:
            max_rate = rate
            peak_column = col
    
    if not peak_column:
        return None
    
    # Extract period years from column name
    _, start_year, end_year = peak_column.split('_')[-3:]
    
    # Get ranking for peak period
    period_ranking = df.sort_values(peak_column, ascending=False).reset_index(drop=True)
    position = period_ranking[period_ranking['Estado'] == state_code].index[0] + 1
    
    # Get regional ranking if needed
    regional_position = None
    if 5 < position < total_states - 2:
        df_region = df[df['Grande-regiao'] == region]
        df_region = df_region.sort_values(peak_column, ascending=False).reset_index(drop=True)
        regional_position = df_region[df_region['Estado'] == state_code].index[0] + 1
    
    # Generate description using common text utils
    ranking_text = get_ranking_description(position, total_states, regional_position, region)
    
    return (
        f"Neste período entre {start_year} e {end_year}, o {state_name} "
        f"{ranking_text.lower()}"
    )
