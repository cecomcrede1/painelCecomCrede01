# --------------------------------------------------------------------------
# RANKING E SELETORES - AVALIECE1
# --------------------------------------------------------------------------

import streamlit as st
import pandas as pd
from typing import List, Dict, Optional, Tuple
from config_api import config_api

class GerenciadorRankingSeletores:
    """Gerenciador para rankings e seletores de escolas e turmas"""
    
    def __init__(self):
        self.escola_selecionada = None
        self.turma_selecionada = None
    
    def renderizar_ranking_escolas(self, df_geral: pd.DataFrame, df_habilidades: pd.DataFrame = None) -> Optional[str]:
        """
        Renderiza ranking de escolas e retorna a escola selecionada
        
        Args:
            df_geral: DataFrame com dados gerais
            df_habilidades: DataFrame com dados de habilidades (opcional)
            
        Returns:
            Código da escola selecionada ou None
        """
        if df_geral.empty:
            st.warning("Nenhum dado disponível para ranking de escolas.")
            return None
        
        st.subheader("🏫 Ranking de Escolas")
        
        # Verificar se temos dados de escolas
        if 'NM_INSTITUICAO' not in df_geral.columns or 'CD_ENTIDADE' not in df_geral.columns:
            st.warning("Dados de escolas (NM_INSTITUICAO) não disponíveis para ranking.")
            return None
        
        # Seletor de critério de ranking
        criterio_ranking = self._renderizar_seletor_criterio_ranking(df_habilidades, "escolas")
        
        # Calcular métricas por escola
        metricas_escolas = self._calcular_metricas_escolas(df_geral, df_habilidades, criterio_ranking)
        
        if metricas_escolas.empty:
            st.warning("Não foi possível calcular métricas das escolas.")
            return None
        
        # Exibir ranking
        self._exibir_ranking_escolas(metricas_escolas, criterio_ranking)
        
        # Seletor de escola
        return self._renderizar_seletor_escola(metricas_escolas)
    
    def renderizar_ranking_turmas(self, df_geral: pd.DataFrame, escola_codigo: str, df_habilidades: pd.DataFrame = None) -> Optional[str]:
        """
        Renderiza ranking de turmas da escola selecionada
        
        Args:
            df_geral: DataFrame com dados gerais
            escola_codigo: Código da escola selecionada
            df_habilidades: DataFrame com dados de habilidades (opcional)
            
        Returns:
            Código da turma selecionada ou None
        """
        if df_geral.empty or not escola_codigo:
            return None
        
        st.subheader("👨‍🏫 Ranking de Turmas")
        
        # Filtrar dados da escola selecionada
        df_escola = df_geral[df_geral['CD_ENTIDADE'] == escola_codigo]
        
        if df_escola.empty:
            st.warning(f"Nenhum dado encontrado para a escola {escola_codigo}")
            return None
        
        # Verificar se temos dados de turmas
        if 'CD_TURMA' not in df_escola.columns or 'NM_TURMA' not in df_escola.columns:
            st.warning("Dados de turmas não disponíveis para ranking.")
            return None
        
        # Seletor de critério de ranking
        criterio_ranking = self._renderizar_seletor_criterio_ranking(df_habilidades, "turmas_escola")
        
        # Calcular métricas por turma
        metricas_turmas = self._calcular_metricas_turmas(df_escola, df_habilidades, criterio_ranking)
        
        if metricas_turmas.empty:
            st.warning("Não foi possível calcular métricas das turmas.")
            return None
        
        # Exibir ranking
        self._exibir_ranking_turmas(metricas_turmas, criterio_ranking)
        
        # Seletor de turma
        return self._renderizar_seletor_turma(metricas_turmas)
    
    def _renderizar_seletor_criterio_ranking(self, df_habilidades: pd.DataFrame = None, key_suffix: str = "") -> str:
        """
        Renderiza seletor de critério de ranking
        
        Args:
            df_habilidades: DataFrame com dados de habilidades
            key_suffix: Sufixo para tornar a chave única
            
        Returns:
            Critério de ranking selecionado
        """
        st.markdown("##### 📊 Critério de Ranking")
        
        # Opções de critério de ranking
        opcoes_criterio = {
            'proficiencia': 'Proficiência Média',
            'participacao': 'Taxa de Participação',
            'total_alunos': 'Total de Alunos'
        }
        
        # Se temos dados de habilidades, adicionar opções de habilidades
        if df_habilidades is not None and not df_habilidades.empty and 'DC_HABILIDADE' in df_habilidades.columns:
            habilidades_disponiveis = df_habilidades['DC_HABILIDADE'].unique()
            for habilidade in habilidades_disponiveis[:10]:  # Limitar a 10 habilidades para não sobrecarregar
                opcoes_criterio[f'habilidade_{habilidade}'] = f'Habilidade: {habilidade}'
        
        # Seletor de critério com chave única
        criterio_selecionado = st.selectbox(
            "Escolha o critério para ranquear:",
            options=list(opcoes_criterio.keys()),
            format_func=lambda x: opcoes_criterio[x],
            help="Selecione por qual métrica ou habilidade deseja ranquear as escolas/turmas",
            key=f"criterio_ranking_{key_suffix}"
        )
        
        return criterio_selecionado
    
    def _adicionar_valores_habilidades(self, metrica: dict, df_habilidades: pd.DataFrame, identificador: str, campo_identificador: str):
        """
        Adiciona valores das habilidades para exibição na tabela
        
        Args:
            metrica: Dicionário com métricas da escola/turma
            df_habilidades: DataFrame com dados de habilidades
            identificador: Código da escola ou turma
            campo_identificador: Campo para identificar (CD_ENTIDADE ou CD_TURMA)
        """
        if df_habilidades is None or df_habilidades.empty:
            return
        
        # Filtrar habilidades para a escola/turma específica
        df_habilidades_filtrado = df_habilidades[df_habilidades[campo_identificador] == identificador]
        
        if df_habilidades_filtrado.empty:
            return
        
        # Obter habilidades únicas
        habilidades_unicas = df_habilidades_filtrado['DC_HABILIDADE'].unique()
        
        # Adicionar valores das habilidades ao dicionário de métricas
        for habilidade in habilidades_unicas[:5]:  # Limitar a 5 habilidades para não sobrecarregar
            df_habilidade = df_habilidades_filtrado[df_habilidades_filtrado['DC_HABILIDADE'] == habilidade]
            
            if not df_habilidade.empty and 'TX_ACERTO' in df_habilidade.columns:
                valor_habilidade = df_habilidade['TX_ACERTO'].mean()
                # Criar nome da coluna para a habilidade
                nome_coluna = f'HABILIDADE_{habilidade.replace(" ", "_").replace(":", "").replace(",", "").replace("(", "").replace(")", "")[:20]}'
                metrica[nome_coluna] = round(valor_habilidade, 1)
    
    def _calcular_metricas_escolas(self, df_geral: pd.DataFrame, df_habilidades: pd.DataFrame = None, criterio_ranking: str = 'proficiencia') -> pd.DataFrame:
        """Calcula métricas para ranking de escolas"""
        metricas = []
        
        for escola in df_geral['CD_ENTIDADE'].unique():
            df_escola = df_geral[df_geral['CD_ENTIDADE'] == escola]
            
            # Calcular métricas básicas
            metrica = {
                'CD_ENTIDADE': escola,
                'NM_INSTITUICAO': df_escola['NM_INSTITUICAO'].iloc[0] if 'NM_INSTITUICAO' in df_escola.columns else 'N/A',
                'TOTAL_CICLOS': len(df_escola['Ciclo'].unique()),
                'MEDIA_PROFICIENCIA': df_escola['AVG_PROFICIENCIA_E1'].mean() if 'AVG_PROFICIENCIA_E1' in df_escola.columns else 0,
                'MEDIA_PARTICIPACAO': df_escola['TX_PARTICIPACAO'].mean() if 'TX_PARTICIPACAO' in df_escola.columns else 0,
                'TOTAL_ALUNOS': df_escola['QT_ALUNO_EFETIVO'].sum() if 'QT_ALUNO_EFETIVO' in df_escola.columns else 0
            }
            
            # Calcular métrica específica do critério de ranking
            if criterio_ranking == 'proficiencia':
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PROFICIENCIA']
                metrica['NOME_CRITERIO'] = 'Proficiência Média'
            elif criterio_ranking == 'participacao':
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PARTICIPACAO']
                metrica['NOME_CRITERIO'] = 'Taxa de Participação'
            elif criterio_ranking == 'total_alunos':
                metrica['CRITERIO_RANKING'] = metrica['TOTAL_ALUNOS']
                metrica['NOME_CRITERIO'] = 'Total de Alunos'
            elif criterio_ranking.startswith('habilidade_') and df_habilidades is not None:
                # Calcular média da habilidade específica
                habilidade_nome = criterio_ranking.replace('habilidade_', '')
                df_habilidade_escola = df_habilidades[df_habilidades['CD_ENTIDADE'] == escola]
                df_habilidade_especifica = df_habilidade_escola[df_habilidade_escola['DC_HABILIDADE'] == habilidade_nome]
                
                if not df_habilidade_especifica.empty and 'TX_ACERTO' in df_habilidade_especifica.columns:
                    metrica['CRITERIO_RANKING'] = df_habilidade_especifica['TX_ACERTO'].mean()
                    metrica['NOME_CRITERIO'] = f'Habilidade: {habilidade_nome}'
                    
                    # Adicionar valores das habilidades para exibição
                    self._adicionar_valores_habilidades(metrica, df_habilidades, escola, 'CD_ENTIDADE')
                else:
                    metrica['CRITERIO_RANKING'] = 0
                    metrica['NOME_CRITERIO'] = f'Habilidade: {habilidade_nome}'
            else:
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PROFICIENCIA']
                metrica['NOME_CRITERIO'] = 'Proficiência Média'
            
            metricas.append(metrica)
        
        df_metricas = pd.DataFrame(metricas)
        
        # Ordenar pelo critério de ranking (descendente)
        if 'CRITERIO_RANKING' in df_metricas.columns:
            df_metricas = df_metricas.sort_values('CRITERIO_RANKING', ascending=False)
        
        return df_metricas
    
    def _calcular_metricas_turmas(self, df_escola: pd.DataFrame, df_habilidades: pd.DataFrame = None, criterio_ranking: str = 'proficiencia') -> pd.DataFrame:
        """Calcula métricas para ranking de turmas"""
        metricas = []
        
        for turma in df_escola['CD_TURMA'].unique():
            df_turma = df_escola[df_escola['CD_TURMA'] == turma]
            
            # Calcular métricas básicas
            metrica = {
                'CD_TURMA': turma,
                'NM_TURMA': df_turma['NM_TURMA'].iloc[0] if 'NM_TURMA' in df_turma.columns else f'Turma {turma}',
                'TOTAL_CICLOS': len(df_turma['Ciclo'].unique()),
                'MEDIA_PROFICIENCIA': df_turma['AVG_PROFICIENCIA_E1'].mean() if 'AVG_PROFICIENCIA_E1' in df_turma.columns else 0,
                'MEDIA_PARTICIPACAO': df_turma['TX_PARTICIPACAO'].mean() if 'TX_PARTICIPACAO' in df_turma.columns else 0,
                'TOTAL_ALUNOS': df_turma['QT_ALUNO_EFETIVO'].sum() if 'QT_ALUNO_EFETIVO' in df_turma.columns else 0
            }
            
            # Calcular métrica específica do critério de ranking
            if criterio_ranking == 'proficiencia':
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PROFICIENCIA']
                metrica['NOME_CRITERIO'] = 'Proficiência Média'
            elif criterio_ranking == 'participacao':
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PARTICIPACAO']
                metrica['NOME_CRITERIO'] = 'Taxa de Participação'
            elif criterio_ranking == 'total_alunos':
                metrica['CRITERIO_RANKING'] = metrica['TOTAL_ALUNOS']
                metrica['NOME_CRITERIO'] = 'Total de Alunos'
            elif criterio_ranking.startswith('habilidade_') and df_habilidades is not None:
                # Calcular média da habilidade específica
                habilidade_nome = criterio_ranking.replace('habilidade_', '')
                df_habilidade_turma = df_habilidades[df_habilidades['CD_TURMA'] == turma]
                df_habilidade_especifica = df_habilidade_turma[df_habilidade_turma['DC_HABILIDADE'] == habilidade_nome]
                
                if not df_habilidade_especifica.empty and 'TX_ACERTO' in df_habilidade_especifica.columns:
                    metrica['CRITERIO_RANKING'] = df_habilidade_especifica['TX_ACERTO'].mean()
                    metrica['NOME_CRITERIO'] = f'Habilidade: {habilidade_nome}'
                    
                    # Adicionar valores das habilidades para exibição
                    self._adicionar_valores_habilidades(metrica, df_habilidades, turma, 'CD_TURMA')
                else:
                    metrica['CRITERIO_RANKING'] = 0
                    metrica['NOME_CRITERIO'] = f'Habilidade: {habilidade_nome}'
            else:
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PROFICIENCIA']
                metrica['NOME_CRITERIO'] = 'Proficiência Média'
            
            metricas.append(metrica)
        
        df_metricas = pd.DataFrame(metricas)
        
        # Ordenar pelo critério de ranking (descendente)
        if 'CRITERIO_RANKING' in df_metricas.columns:
            df_metricas = df_metricas.sort_values('CRITERIO_RANKING', ascending=False)
        
        return df_metricas
    
    def _calcular_metricas_turmas_municipais(self, df_geral: pd.DataFrame, df_habilidades: pd.DataFrame = None, criterio_ranking: str = 'proficiencia') -> pd.DataFrame:
        """Calcula métricas para ranking de turmas municipais"""
        metricas = []
        
        for turma in df_geral['CD_TURMA'].unique():
            df_turma = df_geral[df_geral['CD_TURMA'] == turma]
            
            # Calcular métricas básicas
            metrica = {
                'CD_TURMA': turma,
                'NM_TURMA': df_turma['NM_TURMA'].iloc[0] if 'NM_TURMA' in df_turma.columns else f'Turma {turma}',
                'CD_ENTIDADE': df_turma['CD_ENTIDADE'].iloc[0] if 'CD_ENTIDADE' in df_turma.columns else 'N/A',
                'NM_INSTITUICAO': df_turma['NM_INSTITUICAO'].iloc[0] if 'NM_INSTITUICAO' in df_turma.columns else 'N/A',
                'TOTAL_CICLOS': len(df_turma['Ciclo'].unique()),
                'MEDIA_PROFICIENCIA': df_turma['AVG_PROFICIENCIA_E1'].mean() if 'AVG_PROFICIENCIA_E1' in df_turma.columns else 0,
                'MEDIA_PARTICIPACAO': df_turma['TX_PARTICIPACAO'].mean() if 'TX_PARTICIPACAO' in df_turma.columns else 0,
                'TOTAL_ALUNOS': df_turma['QT_ALUNO_EFETIVO'].sum() if 'QT_ALUNO_EFETIVO' in df_turma.columns else 0
            }
            
            # Calcular métrica específica do critério de ranking
            if criterio_ranking == 'proficiencia':
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PROFICIENCIA']
                metrica['NOME_CRITERIO'] = 'Proficiência Média'
            elif criterio_ranking == 'participacao':
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PARTICIPACAO']
                metrica['NOME_CRITERIO'] = 'Taxa de Participação'
            elif criterio_ranking == 'total_alunos':
                metrica['CRITERIO_RANKING'] = metrica['TOTAL_ALUNOS']
                metrica['NOME_CRITERIO'] = 'Total de Alunos'
            elif criterio_ranking.startswith('habilidade_') and df_habilidades is not None:
                # Calcular média da habilidade específica
                habilidade_nome = criterio_ranking.replace('habilidade_', '')
                df_habilidade_turma = df_habilidades[df_habilidades['CD_TURMA'] == turma]
                df_habilidade_especifica = df_habilidade_turma[df_habilidade_turma['DC_HABILIDADE'] == habilidade_nome]
                
                if not df_habilidade_especifica.empty and 'TX_ACERTO' in df_habilidade_especifica.columns:
                    metrica['CRITERIO_RANKING'] = df_habilidade_especifica['TX_ACERTO'].mean()
                    metrica['NOME_CRITERIO'] = f'Habilidade: {habilidade_nome}'
                    
                    # Adicionar valores das habilidades para exibição
                    self._adicionar_valores_habilidades(metrica, df_habilidades, turma, 'CD_TURMA')
                else:
                    metrica['CRITERIO_RANKING'] = 0
                    metrica['NOME_CRITERIO'] = f'Habilidade: {habilidade_nome}'
            else:
                metrica['CRITERIO_RANKING'] = metrica['MEDIA_PROFICIENCIA']
                metrica['NOME_CRITERIO'] = 'Proficiência Média'
            
            metricas.append(metrica)
        
        df_metricas = pd.DataFrame(metricas)
        
        # Ordenar pelo critério de ranking (descendente)
        if 'CRITERIO_RANKING' in df_metricas.columns:
            df_metricas = df_metricas.sort_values('CRITERIO_RANKING', ascending=False)
        
        return df_metricas
    
    def _exibir_ranking_turmas_municipais(self, df_metricas: pd.DataFrame, criterio_ranking: str = 'proficiencia'):
        """Exibe ranking municipal de turmas"""
        if df_metricas.empty:
            st.warning("Nenhuma turma encontrada para exibir ranking municipal.")
            return
            
        # Preparar dados para exibição
        df_display = df_metricas.copy()
        df_display['POSICAO'] = range(1, len(df_display) + 1)
        
        # Selecionar colunas para exibição
        colunas_display = ['POSICAO', 'NM_TURMA', 'NM_INSTITUICAO', 'CRITERIO_RANKING', 'MEDIA_PROFICIENCIA', 'MEDIA_PARTICIPACAO', 'TOTAL_ALUNOS']
        
        # Adicionar colunas de habilidades se existirem
        colunas_habilidades = [col for col in df_display.columns if col.startswith('HABILIDADE_')]
        colunas_display.extend(colunas_habilidades)
        
        colunas_existentes = [col for col in colunas_display if col in df_display.columns]
        
        if colunas_existentes:
            # Formatar valores
            if 'CRITERIO_RANKING' in df_display.columns:
                df_display['CRITERIO_RANKING'] = df_display['CRITERIO_RANKING'].round(1)
            if 'MEDIA_PROFICIENCIA' in df_display.columns:
                df_display['MEDIA_PROFICIENCIA'] = df_display['MEDIA_PROFICIENCIA'].round(1)
            if 'MEDIA_PARTICIPACAO' in df_display.columns:
                df_display['MEDIA_PARTICIPACAO'] = df_display['MEDIA_PARTICIPACAO'].round(1)
            
            # Obter nome do critério
            nome_criterio = df_display['NOME_CRITERIO'].iloc[0] if 'NOME_CRITERIO' in df_display.columns else 'Critério de Ranking'
            
            # Renomear colunas básicas
            df_display = df_display.rename(columns={
                'POSICAO': 'Posição',
                'NM_TURMA': 'Turma',
                'NM_INSTITUICAO': 'Escola',
                'CRITERIO_RANKING': nome_criterio
            })
            
            # Renomear colunas adicionais apenas se não forem o critério principal
            if nome_criterio != 'Proficiência Média' and 'MEDIA_PROFICIENCIA' in df_display.columns:
                df_display = df_display.rename(columns={'MEDIA_PROFICIENCIA': 'Proficiência Média'})
            if nome_criterio != 'Taxa de Participação' and 'MEDIA_PARTICIPACAO' in df_display.columns:
                df_display = df_display.rename(columns={'MEDIA_PARTICIPACAO': 'Participação Média'})
            if nome_criterio != 'Total de Alunos' and 'TOTAL_ALUNOS' in df_display.columns:
                df_display = df_display.rename(columns={'TOTAL_ALUNOS': 'Total de Alunos'})
            
            # Renomear colunas de habilidades
            for col in df_display.columns:
                if col.startswith('HABILIDADE_'):
                    nome_habilidade = col.replace('HABILIDADE_', '').replace('_', ' ')
                    df_display = df_display.rename(columns={col: nome_habilidade})
            
            # Selecionar colunas para exibição
            colunas_exibicao = ['Posição', 'Turma', 'Escola', nome_criterio]
            
            # Adicionar colunas adicionais se não forem o critério principal
            if nome_criterio != 'Proficiência Média' and 'Proficiência Média' in df_display.columns:
                colunas_exibicao.append('Proficiência Média')
            if nome_criterio != 'Taxa de Participação' and 'Participação Média' in df_display.columns:
                colunas_exibicao.append('Participação Média')
            if nome_criterio != 'Total de Alunos' and 'Total de Alunos' in df_display.columns:
                colunas_exibicao.append('Total de Alunos')
            
            # Adicionar colunas de habilidades
            colunas_habilidades_renomeadas = [col for col in df_display.columns if not col.startswith(('Posição', 'Turma', 'Escola', 'Proficiência Média', 'Participação Média', 'Total de Alunos')) and col != nome_criterio]
            colunas_exibicao.extend(colunas_habilidades_renomeadas)
            
            colunas_finais = [col for col in colunas_exibicao if col in df_display.columns]
            
            st.dataframe(
                df_display[colunas_finais],
                use_container_width=True,
                hide_index=True
            )
    
    def _exibir_ranking_escolas(self, df_metricas: pd.DataFrame, criterio_ranking: str = 'proficiencia'):
        """Exibe ranking de escolas"""
        if df_metricas.empty:
            st.warning("Nenhuma escola encontrada para exibir ranking.")
            return
            
        # Preparar dados para exibição
        df_display = df_metricas.copy()
        df_display['POSICAO'] = range(1, len(df_display) + 1)
        
        # Selecionar colunas para exibição
        colunas_display = ['POSICAO', 'NM_INSTITUICAO', 'CRITERIO_RANKING', 'MEDIA_PROFICIENCIA', 'MEDIA_PARTICIPACAO', 'TOTAL_ALUNOS']
        
        # Adicionar colunas de habilidades se existirem
        colunas_habilidades = [col for col in df_display.columns if col.startswith('HABILIDADE_')]
        colunas_display.extend(colunas_habilidades)
        
        colunas_existentes = [col for col in colunas_display if col in df_display.columns]
        
        if colunas_existentes:
            # Formatar valores
            if 'CRITERIO_RANKING' in df_display.columns:
                df_display['CRITERIO_RANKING'] = df_display['CRITERIO_RANKING'].round(1)
            if 'MEDIA_PROFICIENCIA' in df_display.columns:
                df_display['MEDIA_PROFICIENCIA'] = df_display['MEDIA_PROFICIENCIA'].round(1)
            if 'MEDIA_PARTICIPACAO' in df_display.columns:
                df_display['MEDIA_PARTICIPACAO'] = df_display['MEDIA_PARTICIPACAO'].round(1)
            
            # Obter nome do critério
            nome_criterio = df_display['NOME_CRITERIO'].iloc[0] if 'NOME_CRITERIO' in df_display.columns else 'Critério de Ranking'
            
            # Renomear colunas básicas
            df_display = df_display.rename(columns={
                'POSICAO': 'Posição',
                'NM_INSTITUICAO': 'Escola',
                'CRITERIO_RANKING': nome_criterio
            })
            
            # Renomear colunas adicionais apenas se não forem o critério principal
            if nome_criterio != 'Proficiência Média' and 'MEDIA_PROFICIENCIA' in df_display.columns:
                df_display = df_display.rename(columns={'MEDIA_PROFICIENCIA': 'Proficiência Média'})
            if nome_criterio != 'Taxa de Participação' and 'MEDIA_PARTICIPACAO' in df_display.columns:
                df_display = df_display.rename(columns={'MEDIA_PARTICIPACAO': 'Participação Média'})
            if nome_criterio != 'Total de Alunos' and 'TOTAL_ALUNOS' in df_display.columns:
                df_display = df_display.rename(columns={'TOTAL_ALUNOS': 'Total de Alunos'})
            
            # Renomear colunas de habilidades
            for col in df_display.columns:
                if col.startswith('HABILIDADE_'):
                    nome_habilidade = col.replace('HABILIDADE_', '').replace('_', ' ')
                    df_display = df_display.rename(columns={col: nome_habilidade})
            
            # Selecionar colunas para exibição
            colunas_exibicao = ['Posição', 'Escola', nome_criterio]
            
            # Adicionar colunas adicionais se não forem o critério principal
            if nome_criterio != 'Proficiência Média' and 'Proficiência Média' in df_display.columns:
                colunas_exibicao.append('Proficiência Média')
            if nome_criterio != 'Taxa de Participação' and 'Participação Média' in df_display.columns:
                colunas_exibicao.append('Participação Média')
            if nome_criterio != 'Total de Alunos' and 'Total de Alunos' in df_display.columns:
                colunas_exibicao.append('Total de Alunos')
            
            # Adicionar colunas de habilidades
            colunas_habilidades_renomeadas = [col for col in df_display.columns if not col.startswith(('Posição', 'Escola', 'Proficiência Média', 'Participação Média', 'Total de Alunos')) and col != nome_criterio]
            colunas_exibicao.extend(colunas_habilidades_renomeadas)
            
            colunas_finais = [col for col in colunas_exibicao if col in df_display.columns]
            
            st.dataframe(
                df_display[colunas_finais],
                use_container_width=True,
                hide_index=True
            )
    
    def _exibir_ranking_turmas(self, df_metricas: pd.DataFrame, criterio_ranking: str = 'proficiencia'):
        """Exibe ranking de turmas"""
        if df_metricas.empty:
            st.warning("Nenhuma turma encontrada para exibir ranking.")
            return
            
        # Preparar dados para exibição
        df_display = df_metricas.copy()
        df_display['POSICAO'] = range(1, len(df_display) + 1)
        
        # Selecionar colunas para exibição
        colunas_display = ['POSICAO', 'NM_TURMA', 'CRITERIO_RANKING', 'MEDIA_PROFICIENCIA', 'MEDIA_PARTICIPACAO', 'TOTAL_ALUNOS']
        
        # Adicionar colunas de habilidades se existirem
        colunas_habilidades = [col for col in df_display.columns if col.startswith('HABILIDADE_')]
        colunas_display.extend(colunas_habilidades)
        
        colunas_existentes = [col for col in colunas_display if col in df_display.columns]
        
        if colunas_existentes:
            # Formatar valores
            if 'CRITERIO_RANKING' in df_display.columns:
                df_display['CRITERIO_RANKING'] = df_display['CRITERIO_RANKING'].round(1)
            if 'MEDIA_PROFICIENCIA' in df_display.columns:
                df_display['MEDIA_PROFICIENCIA'] = df_display['MEDIA_PROFICIENCIA'].round(1)
            if 'MEDIA_PARTICIPACAO' in df_display.columns:
                df_display['MEDIA_PARTICIPACAO'] = df_display['MEDIA_PARTICIPACAO'].round(1)
            
            # Obter nome do critério
            nome_criterio = df_display['NOME_CRITERIO'].iloc[0] if 'NOME_CRITERIO' in df_display.columns else 'Critério de Ranking'
            
            # Renomear colunas básicas
            df_display = df_display.rename(columns={
                'POSICAO': 'Posição',
                'NM_TURMA': 'Turma',
                'CRITERIO_RANKING': nome_criterio
            })
            
            # Renomear colunas adicionais apenas se não forem o critério principal
            if nome_criterio != 'Proficiência Média' and 'MEDIA_PROFICIENCIA' in df_display.columns:
                df_display = df_display.rename(columns={'MEDIA_PROFICIENCIA': 'Proficiência Média'})
            if nome_criterio != 'Taxa de Participação' and 'MEDIA_PARTICIPACAO' in df_display.columns:
                df_display = df_display.rename(columns={'MEDIA_PARTICIPACAO': 'Participação Média'})
            if nome_criterio != 'Total de Alunos' and 'TOTAL_ALUNOS' in df_display.columns:
                df_display = df_display.rename(columns={'TOTAL_ALUNOS': 'Total de Alunos'})
            
            # Renomear colunas de habilidades
            for col in df_display.columns:
                if col.startswith('HABILIDADE_'):
                    nome_habilidade = col.replace('HABILIDADE_', '').replace('_', ' ')
                    df_display = df_display.rename(columns={col: nome_habilidade})
            
            # Selecionar colunas para exibição
            colunas_exibicao = ['Posição', 'Turma', nome_criterio]
            
            # Adicionar colunas adicionais se não forem o critério principal
            if nome_criterio != 'Proficiência Média' and 'Proficiência Média' in df_display.columns:
                colunas_exibicao.append('Proficiência Média')
            if nome_criterio != 'Taxa de Participação' and 'Participação Média' in df_display.columns:
                colunas_exibicao.append('Participação Média')
            if nome_criterio != 'Total de Alunos' and 'Total de Alunos' in df_display.columns:
                colunas_exibicao.append('Total de Alunos')
            
            # Adicionar colunas de habilidades
            colunas_habilidades_renomeadas = [col for col in df_display.columns if not col.startswith(('Posição', 'Turma', 'Proficiência Média', 'Participação Média', 'Total de Alunos')) and col != nome_criterio]
            colunas_exibicao.extend(colunas_habilidades_renomeadas)
            
            colunas_finais = [col for col in colunas_exibicao if col in df_display.columns]
            
            st.dataframe(
                df_display[colunas_finais],
                use_container_width=True,
                hide_index=True
            )
    
    def _renderizar_seletor_escola(self, df_metricas: pd.DataFrame) -> Optional[str]:
        """Renderiza seletor de escola"""
        if df_metricas.empty:
            return None
        
        # Criar opções para o selectbox
        opcoes_escola = []
        for _, row in df_metricas.iterrows():
            nome_escola = row.get('NM_INSTITUICAO', f"Escola {row['CD_ENTIDADE']}")
            opcoes_escola.append(f"{row['CD_ENTIDADE']} - {nome_escola}")
        
        # Seletor de escola
        escola_selecionada = st.selectbox(
            "Selecione uma escola para análise detalhada:",
            options=opcoes_escola,
            help="Escolha uma escola do ranking para visualizar gráficos específicos"
        )
        
        if escola_selecionada:
            # Extrair código da escola
            codigo_escola = escola_selecionada.split(" - ")[0]
            self.escola_selecionada = codigo_escola
            return codigo_escola
        
        return None
    
    def _renderizar_seletor_turma(self, df_metricas: pd.DataFrame) -> Optional[str]:
        """Renderiza seletor de turma"""
        if df_metricas.empty:
            return None
        
        # Criar opções para o selectbox
        opcoes_turma = []
        for _, row in df_metricas.iterrows():
            nome_turma = row.get('NM_TURMA', f"Turma {row['CD_TURMA']}")
            opcoes_turma.append(f"{row['CD_TURMA']} - {nome_turma}")
        
        # Seletor de turma
        turma_selecionada = st.selectbox(
            "Selecione uma turma para análise detalhada:",
            options=opcoes_turma,
            help="Escolha uma turma do ranking para visualizar gráficos específicos"
        )
        
        if turma_selecionada:
            # Extrair código da turma
            codigo_turma = turma_selecionada.split(" - ")[0]
            self.turma_selecionada = codigo_turma
            return codigo_turma
        
        return None
    
    def get_escola_selecionada(self) -> Optional[str]:
        """Retorna a escola selecionada"""
        return self.escola_selecionada
    
    def get_turma_selecionada(self) -> Optional[str]:
        """Retorna a turma selecionada"""
        return self.turma_selecionada

# Instância global do gerenciador
gerenciador_ranking = GerenciadorRankingSeletores()
