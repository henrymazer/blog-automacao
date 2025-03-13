def generate_projection_graph_paragraph(state_name):
    """
    Generate markdown image reference for the state's population projection graph.
    
    Args:
        state_name (str): Name of the state from LOCAL column
        
    Returns:
        str: Markdown formatted image reference
    """
    image_path = f"D:\\jornalera-marista\\censo-2022\\dados\\estados\\graficos_populacao_estados_2070\\{state_name}.png"
    return f"![Gráfico de projeção populacional do {state_name} até 2070]({image_path})"
