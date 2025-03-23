def generate_fertility_rate_paragraph(data_loader, state_code: str = 'AC') -> str:
    """Generate paragraph about fertility rate impact on population growth.
    
    Args:
        data_loader: DataLoader instance
        state_code: Two-letter state code
        
    Returns:
        Formatted paragraph about fertility rate impact
    """
    return (
        "A queda contínua nas taxas de fecundidade causa a diminuição do número "
        "de crianças entre 0 e 4 anos, como demonstrado no gráfico abaixo:"
    )
