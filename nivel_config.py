# --------------------------------------------------------------------------
# GERENCIADOR DE CONFIGURAÇÕES DE NÍVEL - AVALIECE1
# --------------------------------------------------------------------------

import streamlit as st
from typing import Dict, List, Optional
from config_api import config_nivel, NIVEL_PADRAO

class GerenciadorNivel:
    """Gerenciador para configurações de nível de agregação"""
    
    def __init__(self):
        self.niveis_disponiveis = config_nivel.get_niveis_disponiveis()
        self.nivel_atual = NIVEL_PADRAO
    
    def renderizar_seletor_nivel(self) -> int:
        """
        Renderiza seletor de nível na sidebar
        
        Returns:
            Nível selecionado pelo usuário
        """
        st.sidebar.subheader("⚙️ Configurações de Dados")
        
        # Criar opções para o selectbox
        opcoes_nivel = []
        for nivel, descricao in self.niveis_disponiveis.items():
            opcoes_nivel.append(f"{nivel} - {descricao}")
        
        # Selecionar nível atual
        indice_atual = list(self.niveis_disponiveis.keys()).index(self.nivel_atual)
        
        nivel_selecionado = st.sidebar.selectbox(
            "Nível de Agregação dos Dados",
            options=opcoes_nivel,
            index=indice_atual,
            help="Escolha o nível de detalhamento dos dados:\n"
                 "• Município: Visão consolidada por município\n"
                 "• Escola: Visão detalhada por unidade escolar\n"
                 "• Turma: Visão granular por turma"
        )
        
        # Extrair o nível numérico da seleção
        nivel_escolhido = int(nivel_selecionado.split(" - ")[0])
        
        # Atualizar nível atual
        self.nivel_atual = nivel_escolhido
        
        # Exibir informações sobre o nível selecionado
        self._exibir_info_nivel(nivel_escolhido)
        
        return nivel_escolhido
    
    def _exibir_info_nivel(self, nivel: int):
        """Exibe informações sobre o nível selecionado"""
        config_nivel_atual = config_nivel.get_config_nivel(nivel)
        
        with st.sidebar.expander("ℹ️ Sobre este nível", expanded=False):
            st.info(f"**{config_nivel_atual['tipo_agregacao']}**: {config_nivel_atual['descricao']}")
            
            # Exibir características específicas do nível
            st.markdown("**Características:**")
            for caracteristica in config_nivel_atual['caracteristicas']:
                st.markdown(f"- {caracteristica}")
            
            # Exibir informações adicionais baseadas no tipo
            if nivel == 0:  # Município
                st.markdown("""
                **👥 Público-alvo:**
                - Secretários de Educação
                - Coordenadores Municipais
                - Gestores da Rede
                """)
            elif nivel == 1:  # Escola
                st.markdown("""
                **👥 Público-alvo:**
                - Diretores de Escola
                - Coordenadores Pedagógicos
                - Supervisores Escolares
                """)
            elif nivel == 2:  # Turma
                st.markdown("""
                **👥 Público-alvo:**
                - Professores
                - Coordenadores de Área
                - Especialistas em Educação
                """)
    
    def get_nivel_atual(self) -> int:
        """Retorna o nível atual configurado"""
        return self.nivel_atual
    
    def set_nivel(self, nivel: int):
        """Define um nível específico"""
        if nivel in self.niveis_disponiveis:
            self.nivel_atual = nivel
        else:
            raise ValueError(f"Nível {nivel} não é válido. Níveis disponíveis: {list(self.niveis_disponiveis.keys())}")
    
    def get_config_nivel_atual(self) -> Dict[str, str]:
        """Retorna a configuração do nível atual"""
        return config_nivel.get_config_nivel(self.nivel_atual)
    
    def exibir_comparacao_niveis(self):
        """Exibe comparação entre os diferentes níveis"""
        with st.expander("📊 Comparação entre Níveis de Agregação", expanded=False):
            st.markdown("### Diferenças entre os níveis de agregação:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                **🏛️ Município (Nível 0)**
                - Dados consolidados por município
                - Visão geral da rede municipal
                - Indicadores agregados
                - Ideal para gestão municipal
                
                **👥 Público:** Secretários, Coordenadores Municipais
                """)
            
            with col2:
                st.markdown("""
                **🏫 Escola (Nível 1)**
                - Dados por unidade escolar
                - Detalhamento por escola
                - Análise comparativa entre escolas
                - Ideal para gestão escolar
                
                **👥 Público:** Diretores, Coordenadores Pedagógicos
                """)
            
            with col3:
                st.markdown("""
                **👨‍🏫 Turma (Nível 2)**
                - Dados por turma
                - Máximo detalhamento
                - Análise pedagógica específica
                - Ideal para professores
                
                **👥 Público:** Professores, Especialistas
                """)

# Instância global do gerenciador
gerenciador_nivel = GerenciadorNivel()

# --------------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# --------------------------------------------------------------------------

def obter_nivel_atual() -> int:
    """Função auxiliar para obter o nível atual"""
    return gerenciador_nivel.get_nivel_atual()

def definir_nivel(nivel: int):
    """Função auxiliar para definir um nível específico"""
    gerenciador_nivel.set_nivel(nivel)

def obter_config_nivel_atual() -> Dict[str, str]:
    """Função auxiliar para obter configuração do nível atual"""
    return gerenciador_nivel.get_config_nivel_atual()
