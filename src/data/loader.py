import pandas as pd

def load_census_data():
    """Load and prepare census data from CSV files."""
    # Load ranking data
    df = pd.read_csv(r"D:\jornalera-marista\censo-2022\dados\estados\Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv")
    
    # Load growth data
    df_crescimento = pd.read_csv(r"D:\jornalera-marista\censo-2022\dados\estados\compilado_estados.csv")
    
    return df, df_crescimento

def get_state_data(df, state_code='AC'):
    """Get state-specific data from the dataframe."""
    primeira_linha = df.iloc[0] if state_code == 'AC' else df[df['Estado'] == state_code].iloc[0]
    
    return {
        'nome_estado': primeira_linha['LOCAL'],
        'regiao': primeira_linha['Grande-regiao']
    }

def get_first_census_data(df, state_code='AC'):
    """Get the first available census data for a state."""
    primeira_linha = df.iloc[0] if state_code == 'AC' else df[df['Estado'] == state_code].iloc[0]
    
    # Lista de colunas para verificar
    colunas_censo = [col for col in ['1872', '1890', '1900', '1910', '1920', '1940', '1950', '1960'] 
                     if col in df.columns]
    
    # Encontrar a primeira coluna com dados
    for coluna in colunas_censo:
        valor = primeira_linha[coluna]
        if pd.notna(valor) and valor != 0:
            return {
                'ano': coluna,
                'valor': valor
            }
    
    return None

def get_growth_data(df_crescimento, state_code='AC'):
    """Get growth data for a state."""
    return df_crescimento.loc[df_crescimento['Estado'] == state_code, 'x_crescimento'].iloc[0]

def get_ranking_data(df_crescimento, state_code='AC'):
    """Get ranking data for a state."""
    # Ordenar estados por crescimento
    df_ranking = df_crescimento.sort_values('x_crescimento', ascending=False).reset_index(drop=True)
    posicao = df_ranking[df_ranking['Estado'] == state_code].index[0] + 1
    total_estados = len(df_crescimento)
    
    return {
        'posicao': posicao,
        'total_estados': total_estados
    }

def get_regional_ranking(df_crescimento, regiao, state_code='AC'):
    """Get regional ranking data for a state."""
    df_regiao = df_crescimento[df_crescimento['Grande-regiao'] == regiao]\
        .sort_values('x_crescimento', ascending=False)\
        .reset_index(drop=True)
    
    posicao_regiao = df_regiao[df_regiao['Estado'] == state_code].index[0] + 1
    return posicao_regiao
