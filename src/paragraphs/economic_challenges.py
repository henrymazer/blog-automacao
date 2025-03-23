def generate_economic_challenges_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph about economic challenges due to demographic changes.
    
    Args:
        data_loader: DataLoader instance
        state_code: Two-letter state code
        
    Returns:
        Formatted paragraph about economic challenges
    """
    # Get state info
    state_info, _, _, _ = data_loader.get_state_data(state_code)
    state_name = state_info['name']
    
    return (
        f"O principal desafio para a economia do {state_name} será o aumento dos custos de aposentadoria, "
        f"a pressão no sistema de saúde, escolas sem utilização, e as dificuldades para manter a "
        f"produtividade com menos trabalhadores em idade ativa."
    )
