# --------------------------------------------------------------------------
# CONFIGURAÇÕES DA API - AVALIECE1
# --------------------------------------------------------------------------

from dataclasses import dataclass
from typing import Dict, Set, FrozenSet

@dataclass
class ConfigAPI:
    """Configurações da API para diferentes níveis de agregação"""
    
    # URL base da API
    API_URL: str = "https://avaliacaoemonitoramentoceara.caeddigital.net/portal/functions/getDadosResultado"
    
    # Timeout para requisições
    REQUEST_TIMEOUT: int = 30
    
    # Etapas disponíveis
    ETAPAS: Set[int] = frozenset({2, 4, 5, 8, 9})
    
    # Ciclos de avaliação
    CICLOS: Dict[str, str] = frozenset({
        "1": "1º Ciclo",
        "2": "2º Ciclo",
    }.items())
    
    # Componentes curriculares
    COMPONENTES: Dict[str, str] = frozenset({
        "Língua Portuguesa": "LP",
        "Matemática": "MT"
    }.items())
    
    # Escolas indígenas (códigos conhecidos)
    ESCOLAS_INDIGENAS: Set[str] = frozenset({
        "23000291", "23244755", "23239174", "23564067", "23283610", 
        "23215674", "23263423", "23061642", "23462353", "23062770",
        "23241462", "23235411", "23241454", "23215682", "23263555"
    })

class ConfigNivelAgregacao:
    """Configurações específicas para diferentes níveis de agregação"""
    
    def __init__(self):
        """Inicializa as configurações dos níveis"""
        # Nível 0: Município (dados mais agregados)
        self.NIVEL_0 = {
            "nivelAbaixo": "0",
            "descricao": "Município - Visão consolidada por município",
            "tipo_agregacao": "Município",
            "caracteristicas": [
                "Dados consolidados por município",
                "Visão geral da rede municipal",
                "Indicadores agregados",
                "Ideal para gestão municipal"
            ]
        }
        
        # Nível 1: Escola (dados intermediários)
        self.NIVEL_1 = {
            "nivelAbaixo": "1", 
            "descricao": "Escola - Visão detalhada por unidade escolar",
            "tipo_agregacao": "Escola",
            "caracteristicas": [
                "Dados por unidade escolar",
                "Detalhamento por escola",
                "Análise comparativa entre escolas",
                "Ideal para gestão escolar"
            ]
        }
        
        # Nível 2: Turma (dados mais detalhados)
        self.NIVEL_2 = {
            "nivelAbaixo": "2",
            "descricao": "Turma - Visão granular por turma",
            "tipo_agregacao": "Turma",
            "caracteristicas": [
                "Dados por turma",
                "Máximo detalhamento",
                "Análise pedagógica específica",
                "Ideal para professores e coordenadores"
            ]
        }
    
    def get_config_nivel(self, nivel: int) -> Dict[str, str]:
        """Retorna configuração para um nível específico"""
        niveis = {
            0: self.NIVEL_0,
            1: self.NIVEL_1,
            2: self.NIVEL_2
        }
        return niveis.get(nivel, self.NIVEL_0)
    
    def get_niveis_disponiveis(self) -> Dict[int, str]:
        """Retorna todos os níveis disponíveis com suas descrições"""
        return {
            0: self.NIVEL_0["descricao"],
            1: self.NIVEL_1["descricao"], 
            2: self.NIVEL_2["descricao"]
        }

# Instâncias globais das configurações
config_api = ConfigAPI()
config_nivel = ConfigNivelAgregacao()

# Configuração padrão do nível (pode ser alterada facilmente aqui)
NIVEL_PADRAO = 0  # Altere para 0, 1 ou 2 conforme necessário
