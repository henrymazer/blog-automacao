def generate_graph_image_paragraph(state_name):
    """
    Generate markdown image reference for the state's population growth graph.
    
    Args:
        state_name (str): Name of the state from LOCAL column
        
    Returns:
        str: Markdown formatted image reference
    """
    image_path = f"D:\\jornalera-marista\\censo-2022\\dados\\estados\\graphs_pop_2024\\{state_name}.png"
    return f"![Gráfico de crescimento populacional do {state_name}]({image_path})"
