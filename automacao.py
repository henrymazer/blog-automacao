from src.data.loader import DataLoader
from src.utils.api import PerplexityAPI
from src.utils.formatting import BrazilianFormatter
from src.utils.text_utils import (
    get_ranking_description,
    get_creation_description,
    format_historical_info
)

from src.paragraphs.growth import generate_growth_paragraph
from src.paragraphs.ranking import generate_ranking_paragraph
from src.paragraphs.creation import generate_creation_paragraph
from src.paragraphs.historical import generate_historical_paragraph
from src.paragraphs.peak_growth import generate_peak_growth_paragraph
from src.paragraphs.peak_comparison import generate_peak_comparison_paragraph
from src.paragraphs.chart_intro import generate_chart_intro_paragraph
from src.paragraphs.graph_image import generate_graph_image_paragraph
from src.paragraphs.future_header import generate_future_header
from src.paragraphs.population_peak import generate_population_peak_paragraph
from src.paragraphs.projection_graph import generate_projection_graph_paragraph
from src.paragraphs.graph_description import generate_graph_description_paragraph
from src.paragraphs.population_peak_comparison import generate_population_peak_comparison
from src.paragraphs.age_composition_header import generate_age_composition_header
from src.paragraphs.fertility_rate import generate_fertility_rate_paragraph
from src.paragraphs.fertility_graph_image import generate_fertility_graph_image_paragraph
from src.paragraphs.children_population_change import generate_children_population_change_paragraph
from src.paragraphs.elderly_population import generate_elderly_population_paragraph
from src.paragraphs.elderly_graph_image import generate_elderly_graph_image_paragraph
from src.paragraphs.elderly_population_change import generate_elderly_population_change_paragraph
from src.paragraphs.demographic_transition import generate_demographic_transition_paragraph
from src.paragraphs.economic_challenges import generate_economic_challenges_paragraph
from src.paragraphs.retirement_header import generate_retirement_header
from src.paragraphs.retirement_age import generate_retirement_age_paragraph
from src.paragraphs.retirement_projections import generate_retirement_projections_paragraph
from src.paragraphs.saude_header import generate_saude_header
from src.paragraphs.saude_infra import generate_saude_infra_paragraph
from src.paragraphs.saude_cronicos import generate_saude_cronicos_paragraph
from src.paragraphs.saude_atual import generate_saude_atual_paragraph
from src.paragraphs.educacao_header import generate_educacao_header
from src.paragraphs.educacao_alunos import generate_educacao_alunos_paragraph
from src.paragraphs.economia_nacional import generate_economia_nacional_paragraph

# Configuration
RANKING_FILE = r"D:\jornalera-marista\censo-2022\dados\estados\Dados_com_Posi__o_do_Auge_por_Regi_o_ranking.csv"
GROWTH_FILE = r"D:\jornalera-marista\censo-2022\dados\estados\compilado_estados.csv"
AGE_DATA_FILE = r"D:\jornalera-marista\censo-2022\dados\estados\Tabela_Popula__o_por_Faixa_Et_ria_e_Anos.csv"
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise EnvironmentError("A variável de ambiente PERPLEXITY_API_KEY não está definida no arquivo .env")

def generate_article(state_code: str = 'AC') -> None:
    """Generate a complete article for a given state.
    
    Args:
        state_code: Two-letter state code (default: 'AC' for Acre)
    """
    # Initialize components
    data_loader = DataLoader(RANKING_FILE, GROWTH_FILE, AGE_DATA_FILE)
    api_client = PerplexityAPI(API_KEY)
    formatter = BrazilianFormatter()
    
    # 1. Population growth since first census
    growth_text = generate_growth_paragraph(data_loader, state_code)
    if growth_text:
        print(growth_text)
        print()  # Single line break
    
    # 2. Ranking comparison
    ranking_text = generate_ranking_paragraph(data_loader, state_code)
    if ranking_text:
        print(ranking_text)
        print()  # Single line break
    
    # 3. State creation and initial population
    creation_text = generate_creation_paragraph(data_loader, api_client, formatter, state_code)
    if creation_text:
        print(creation_text)
        print()  # Single line break
        
    # 4. Historical context
    historical_text = generate_historical_paragraph(data_loader, api_client, state_code)
    if historical_text:
        print(historical_text)
        print()  # Single line break
    
    # 5. Peak growth period
    peak_growth_text = generate_peak_growth_paragraph(data_loader, state_code)
    if peak_growth_text:
        print(peak_growth_text)
        print()  # Single line break
    
    # 6. Peak growth comparison
    comparison_text = generate_peak_comparison_paragraph(data_loader, state_code)
    if comparison_text:
        print(comparison_text)
        print()  # Single line break
    
    # 7. Chart introduction
    chart_intro_text = generate_chart_intro_paragraph(data_loader, state_code)
    if chart_intro_text:
        print(chart_intro_text)
        print()  # Single line break
    
    # 8. Population graph
    graph_image = generate_graph_image_paragraph(data_loader, state_code)
    if graph_image:
        print(graph_image)
        print()  # Single line break
    
    # 9. Future section header
    future_header = generate_future_header()
    if future_header:
        print("\n" + future_header)  # Double line break before new section
        print()  # Single line break after header
    
    # 10. Population peak projection
    peak_projection = generate_population_peak_paragraph(data_loader, formatter, state_code)
    if peak_projection:
        print(peak_projection)
        print()  # Single line break
    
    # 11. Population projection graph
    projection_graph = generate_projection_graph_paragraph(data_loader, state_code)
    if projection_graph:
        print(projection_graph)
        print()  # Single line break
    
    # 12. Graph description
    graph_description = generate_graph_description_paragraph(data_loader, state_code)
    if graph_description:
        print(graph_description)
        print()  # Single line break
    
    # 13. Population peak comparison
    peak_comparison = generate_population_peak_comparison(data_loader, state_code)
    if peak_comparison:
        print(peak_comparison)
        print()  # Single line break
        
    # 14. Age composition section header
    age_header = generate_age_composition_header()
    if age_header:
        print("\n" + age_header)  # Double line break before new section
        print()  # Single line break after header
        
    # 15. Fertility rate impact
    fertility_text = generate_fertility_rate_paragraph(data_loader, state_code)
    if fertility_text:
        print(fertility_text)
        print()  # Single line break
        
    # 16. Fertility graph image
    fertility_graph_image = generate_fertility_graph_image_paragraph(data_loader, state_code)
    if fertility_graph_image:
        print(fertility_graph_image)
        print()  # Single line break
        
    # 18. Children population change
    children_change = generate_children_population_change_paragraph(data_loader, formatter, state_code)
    if children_change:
        print(children_change)
        print()  # Single line break
        
    # 19. Elderly population growth
    elderly_text = generate_elderly_population_paragraph()
    if elderly_text:
        print(elderly_text)
        print()  # Single line break
        
    # 20. Elderly population graph
    elderly_graph = generate_elderly_graph_image_paragraph(data_loader, state_code)
    if elderly_graph:
        print(elderly_graph)
        print()  # Single line break
        
    # 21. Elderly population change
    elderly_change = generate_elderly_population_change_paragraph(data_loader, formatter, state_code)
    if elderly_change:
        print(elderly_change)
        print()  # Single line break
        
    # 22. Demographic transition explanation
    demographic_text = generate_demographic_transition_paragraph()
    if demographic_text:
        print(demographic_text)
        print()  # Single line break
        
    # 23. Economic challenges
    economic_text = generate_economic_challenges_paragraph(data_loader, state_code)
    if economic_text:
        print(economic_text)
        print()  # Single line break
        
    # 24. Retirement section header
    retirement_header = generate_retirement_header()
    if retirement_header:
        print("\n" + retirement_header)  # Double line break before new section
        print()  # Single line break after header

    # 25. Retirement age paragraph
    retirement_age_paragraph = generate_retirement_age_paragraph()
    if retirement_age_paragraph:
        print(retirement_age_paragraph)
        print()  # Single line break
        
    # 26. Retirement age projections
    retirement_projections = generate_retirement_projections_paragraph()
    if retirement_projections:
        print(retirement_projections)
        print()  # Single line break
        
    # 27. Health section header
    saude_header = generate_saude_header()
    if saude_header:
        print("\n" + saude_header)  # Double line break before new section
        print()  # Single line break after header
        
    # 28. Health infrastructure
    saude_infra = generate_saude_infra_paragraph()
    if saude_infra:
        print(saude_infra)
        print()  # Single line break
        
    # 29. Chronic healthcare needs
    saude_cronicos = generate_saude_cronicos_paragraph()
    if saude_cronicos:
        print(saude_cronicos)
        print()  # Single line break
        
    # 30. Current health system status - VERSÃO ATUALIZADA
    saude_atual = generate_saude_atual_paragraph(data_loader, api_client, state_code)
    if saude_atual:
        # Como temos dois parágrafos separados por \n\n, vamos garantir uma formatação consistente
        paragrafos_saude = saude_atual.split("\n\n")
        
        for i, paragrafo in enumerate(paragrafos_saude):
            if paragrafo.strip():  # Verifica se o parágrafo não está vazio
                print(paragrafo.strip())
                
                # Adiciona quebra de linha após cada parágrafo, exceto o último
                if i < len(paragrafos_saude) - 1:
                    print()  # Single line break
        
        print()  # Garantimos uma linha extra após o último parágrafo da seção
        
    # 31. Education section header
    educacao_header = generate_educacao_header()
    if educacao_header:
        print("\n" + educacao_header)  # Double line break before new section
        print()  # Single line break after header
        
    # 32. Education student numbers
    educacao_alunos = generate_educacao_alunos_paragraph(data_loader, formatter, state_code)
    if educacao_alunos:
        print(educacao_alunos)
        print()  # Single line break
        
    # 33. National economic challenges
    economia_nacional = generate_economia_nacional_paragraph(state_code)
    if economia_nacional:
        print(economia_nacional)

if __name__ == "__main__":
    generate_article()
