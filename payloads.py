# --------------------------------------------------------------------------
# CLASSES DE PAYLOAD PARA API - AVALIECE1
# --------------------------------------------------------------------------

from typing import Dict, List
from dataclasses import dataclass
import indicadores
from config_api import config_api, config_nivel, NIVEL_PADRAO

@dataclass
class PayloadBase:
    """Classe base para payloads da API"""
    entidade: str
    componente: str
    etapa: int
    ciclo: str
    installation_id: str
    session_token: str
    nivel_agregacao: int = None  # Novo parâmetro para nível de agregação
    
    def __post_init__(self):
        """Define o nível padrão se não especificado"""
        if self.nivel_agregacao is None:
            self.nivel_agregacao = NIVEL_PADRAO
    
    def _criar_filtros_base(self) -> List[Dict]:
        """Cria filtros básicos comuns"""
        return [
            {"operation": "equalTo", "field": "DADOS.VL_FILTRO_DISCIPLINA", "value": dict(config_api.COMPONENTES)[self.componente]},
            {"operation": "equalTo", "field": "DADOS.VL_FILTRO_ETAPA", "value": f"ENSINO FUNDAMENTAL DE 9 ANOS - {self.etapa}º ANO", "data": {"NM_ETAPA": f"{self.etapa}º ano do Ensino Fundamental"}},
            {"operation": "equalTo", "field": "DADOS.VL_FILTRO_AVALIACAO", "value": "21351"},
        ]
    
    def _criar_payload_base(self, indicadores_list: List, filtros_extras: List = None) -> Dict:
        """Cria estrutura base do payload"""
        filtros_extras = filtros_extras or []
        
        # Usar valor fixo para rede conforme payload de exemplo
        dependencia = "MUNICIPAL"
        
        # Obter configuração do nível de agregação
        config_nivel_atual = config_nivel.get_config_nivel(self.nivel_agregacao)
        
        return {
            "CD_INDICADOR": indicadores_list,
            "agregado": self.entidade,
            "filtros": [
                {"operation": "equalTo", "field": "DADOS.VL_FILTRO_AVALIACAO", "value": f"{self.ciclo}1351" if self.ciclo == "2" else "20141"},
                {"operation": "equalTo", "field": "DADOS.VL_FILTRO_DISCIPLINA", "value": dict(config_api.COMPONENTES)[self.componente]},
                {"operation": "equalTo", "field": "DADOS.VL_FILTRO_REDE", "value": dependencia},
                {"operation": "equalTo", "field": "DADOS.VL_FILTRO_ETAPA", "value": f"ENSINO FUNDAMENTAL DE 9 ANOS - {self.etapa}º ANO", "data": {"NM_ETAPA": f"{self.etapa}º ano do Ensino Fundamental"}}
            ] + filtros_extras,
            "filtrosAdicionais": [],
            "ordenacao": [["DC_HORARIO", "ASC"]], 
            "nivelAbaixo": config_nivel_atual["nivelAbaixo"],  # Usa configuração do nível
            "collectionResultado": None, 
            "CD_INDICADOR_LABEL": [], 
            "TP_ENTIDADE_LABEL": "01",
            "_ApplicationId": "portal", 
            "_ClientVersion": "js2.19.0", 
            "_InstallationId": self.installation_id,
            "_SessionToken": self.session_token
        }

class PayloadGeral(PayloadBase):
    """Payload para dados gerais"""
    
    def criar_payload(self) -> Dict:
        return self._criar_payload_base(list(indicadores.INDIC_GERAL))

class PayloadHabilidades(PayloadBase):
    """Payload para dados de habilidades"""
    
    def criar_payload(self) -> Dict:
        filtros_extras = [
            {"operation": "containedIn", "field": "DADOS.DC_FAIXA_PERCENTUAL_HABILIDADE", 
             "value": ["Alto", "Médio Baixo", "Médio Alto", "Baixo"]}
        ]
        
        payload = self._criar_payload_base(list(indicadores.INDIC_HABILIDADES), filtros_extras)
        payload["ordenacao"] = [["DADOS.CD_HABILIDADE", "ASC"]]
        
        return payload

# --------------------------------------------------------------------------
# FUNÇÕES AUXILIARES PARA CRIAÇÃO DE PAYLOADS
# --------------------------------------------------------------------------

def criar_payload_geral(entidade: str, componente: str, etapa: int, ciclo: str, 
                       installation_id: str, session_token: str, 
                       nivel_agregacao: int = None) -> Dict:
    """
    Função auxiliar para criar payload geral com nível de agregação específico
    
    Args:
        entidade: Código da entidade (município/escola)
        componente: Componente curricular
        etapa: Etapa de ensino
        ciclo: Ciclo de avaliação
        installation_id: ID de instalação da API
        session_token: Token de sessão da API
        nivel_agregacao: Nível de agregação (0, 1 ou 2). Se None, usa o padrão.
    
    Returns:
        Payload configurado para a API
    """
    payload_obj = PayloadGeral(
        entidade=entidade,
        componente=componente,
        etapa=etapa,
        ciclo=ciclo,
        installation_id=installation_id,
        session_token=session_token,
        nivel_agregacao=nivel_agregacao
    )
    return payload_obj.criar_payload()

def criar_payload_habilidades(entidade: str, componente: str, etapa: int, ciclo: str,
                             installation_id: str, session_token: str,
                             nivel_agregacao: int = None) -> Dict:
    """
    Função auxiliar para criar payload de habilidades com nível de agregação específico
    
    Args:
        entidade: Código da entidade (município/escola)
        componente: Componente curricular
        etapa: Etapa de ensino
        ciclo: Ciclo de avaliação
        installation_id: ID de instalação da API
        session_token: Token de sessão da API
        nivel_agregacao: Nível de agregação (0, 1 ou 2). Se None, usa o padrão.
    
    Returns:
        Payload configurado para a API
    """
    payload_obj = PayloadHabilidades(
        entidade=entidade,
        componente=componente,
        etapa=etapa,
        ciclo=ciclo,
        installation_id=installation_id,
        session_token=session_token,
        nivel_agregacao=nivel_agregacao
    )
    return payload_obj.criar_payload()
