# --------------------------------------------------------------------------
# CONFIGURAÇÕES DE EXEMPLO PARA DIFERENTES NÍVEIS - AVALIECE1
# --------------------------------------------------------------------------

"""
Este arquivo contém exemplos de configurações para diferentes cenários
de uso dos níveis de agregação (nivelAbaixo = 0, 1, 2).

Para usar, copie a configuração desejada para o arquivo config_api.py
"""

# --------------------------------------------------------------------------
# CONFIGURAÇÃO PARA NÍVEL 0 (DADOS AGREGADOS) - PADRÃO ATUAL
# --------------------------------------------------------------------------

CONFIG_NIVEL_0 = {
    "NIVEL_PADRAO": 0,
    "DESCRICAO": "Dados mais agregados - Visão geral",
    "CARACTERISTICAS": [
        "Dados consolidados",
        "Menor volume de informações", 
        "Carregamento mais rápido",
        "Ideal para visão geral"
    ],
    "USO_RECOMENDADO": "Dashboards executivos e análises rápidas"
}

# --------------------------------------------------------------------------
# CONFIGURAÇÃO PARA NÍVEL 1 (DADOS INTERMEDIÁRIOS)
# --------------------------------------------------------------------------

CONFIG_NIVEL_1 = {
    "NIVEL_PADRAO": 1,
    "DESCRICAO": "Dados intermediários - Detalhamento médio",
    "CARACTERISTICAS": [
        "Dados moderados",
        "Detalhamento intermediário",
        "Equilíbrio entre informação e performance",
        "Ideal para análises detalhadas"
    ],
    "USO_RECOMENDADO": "Análises pedagógicas e relatórios técnicos"
}

# --------------------------------------------------------------------------
# CONFIGURAÇÃO PARA NÍVEL 2 (DADOS DETALHADOS)
# --------------------------------------------------------------------------

CONFIG_NIVEL_2 = {
    "NIVEL_PADRAO": 2,
    "DESCRICAO": "Dados mais detalhados - Visão granular",
    "CARACTERISTICAS": [
        "Dados granulares",
        "Máximo detalhamento disponível",
        "Carregamento mais lento",
        "Ideal para análises profundas"
    ],
    "USO_RECOMENDADO": "Pesquisas específicas e estudos detalhados"
}

# --------------------------------------------------------------------------
# INSTRUÇÕES DE USO
# --------------------------------------------------------------------------

def obter_instrucoes():
    """Retorna instruções de como usar as configurações"""
    return """
=== INSTRUÇÕES DE USO ===

Para alterar o nível de agregação:

1. ABRIR O ARQUIVO config_api.py
2. LOCALIZAR A LINHA: NIVEL_PADRAO = 0
3. ALTERAR O VALOR PARA:
   - 0: Dados agregados (padrão atual)
   - 1: Dados intermediários  
   - 2: Dados detalhados
4. SALVAR O ARQUIVO
5. REINICIAR A APLICAÇÃO

ALTERNATIVAMENTE:
- Use o seletor na interface da aplicação
- Ou altere programaticamente usando nivel_config.py
"""

# --------------------------------------------------------------------------
# COMPARAÇÃO RÁPIDA
# --------------------------------------------------------------------------

def comparar_configuracoes():
    """Compara as três configurações disponíveis"""
    print("=== COMPARAÇÃO DOS NÍVEIS ===\n")
    
    configs = [
        ("Nível 0", CONFIG_NIVEL_0),
        ("Nível 1", CONFIG_NIVEL_1), 
        ("Nível 2", CONFIG_NIVEL_2)
    ]
    
    for nome, config in configs:
        print(f"{nome}:")
        print(f"  - Padrão: {config['NIVEL_PADRAO']}")
        print(f"  - Descrição: {config['DESCRICAO']}")
        print(f"  - Uso: {config['USO_RECOMENDADO']}")
        print()

# --------------------------------------------------------------------------
# EXEMPLO DE ALTERAÇÃO AUTOMÁTICA
# --------------------------------------------------------------------------

def exemplo_alteracao_automatica():
    """Exemplo de como alterar automaticamente entre níveis"""
    
    print("=== EXEMPLO DE ALTERAÇÃO AUTOMÁTICA ===\n")
    
    # Simular diferentes cenários
    cenarios = [
        ("Análise Executiva", 0),
        ("Relatório Pedagógico", 1),
        ("Pesquisa Detalhada", 2)
    ]
    
    for cenario, nivel in cenarios:
        print(f"Cenário: {cenario}")
        print(f"Nível recomendado: {nivel}")
        
        if nivel == 0:
            config = CONFIG_NIVEL_0
        elif nivel == 1:
            config = CONFIG_NIVEL_1
        else:
            config = CONFIG_NIVEL_2
            
        print(f"Características: {', '.join(config['CARACTERISTICAS'])}")
        print()

if __name__ == "__main__":
    print("=== CONFIGURAÇÕES DE EXEMPLO - AVALIECE1 ===\n")
    
    comparar_configuracoes()
    exemplo_alteracao_automatica()
    print(obter_instrucoes())
