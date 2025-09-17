# --------------------------------------------------------------------------
# EXEMPLO DE CONFIGURAÇÃO DE NÍVEIS - AVALIECE1
# --------------------------------------------------------------------------

"""
Este arquivo demonstra como alterar facilmente o parâmetro nivelAbaixo
entre os valores 0, 1 e 2 usando a estrutura modularizada.

Para alterar o nível padrão, você tem 3 opções:
"""

# --------------------------------------------------------------------------
# OPÇÃO 1: ALTERAR O NÍVEL PADRÃO NO ARQUIVO DE CONFIGURAÇÃO
# --------------------------------------------------------------------------

# No arquivo config_api.py, altere a linha:
# NIVEL_PADRAO = 0  # Altere para 0, 1 ou 2 conforme necessário

# Exemplos:
# NIVEL_PADRAO = 0  # Dados mais agregados (padrão atual)
# NIVEL_PADRAO = 1  # Dados intermediários
# NIVEL_PADRAO = 2  # Dados mais detalhados

# --------------------------------------------------------------------------
# OPÇÃO 2: ALTERAR PROGRAMATICAMENTE DURANTE A EXECUÇÃO
# --------------------------------------------------------------------------

from nivel_config import gerenciador_nivel, definir_nivel, obter_nivel_atual

# Exemplo de como alterar o nível programaticamente:
def exemplo_alteracao_programatica():
    """Exemplo de como alterar o nível durante a execução"""
    
    # Obter nível atual
    nivel_atual = obter_nivel_atual()
    print(f"Nível atual: {nivel_atual}")
    
    # Alterar para nível 1
    definir_nivel(1)
    print(f"Novo nível: {obter_nivel_atual()}")
    
    # Alterar para nível 2
    definir_nivel(2)
    print(f"Novo nível: {obter_nivel_atual()}")
    
    # Voltar para nível 0
    definir_nivel(0)
    print(f"Nível final: {obter_nivel_atual()}")

# --------------------------------------------------------------------------
# OPÇÃO 3: USAR DIFERENTES NÍVEIS PARA DIFERENTES OPERAÇÕES
# --------------------------------------------------------------------------

from payloads import criar_payload_geral, criar_payload_habilidades

def exemplo_niveis_especificos():
    """Exemplo de como usar diferentes níveis para diferentes operações"""
    
    # Dados de exemplo
    entidade = "23000291"
    componente = "Língua Portuguesa"
    etapa = 5
    ciclo = "1"
    installation_id = "exemplo_id"
    session_token = "exemplo_token"
    
    # Criar payload com nível 0 (agregado)
    payload_nivel_0 = criar_payload_geral(
        entidade, componente, etapa, ciclo,
        installation_id, session_token, nivel_agregacao=0
    )
    print("Payload Nível 0:", payload_nivel_0["nivelAbaixo"])
    
    # Criar payload com nível 1 (intermediário)
    payload_nivel_1 = criar_payload_geral(
        entidade, componente, etapa, ciclo,
        installation_id, session_token, nivel_agregacao=1
    )
    print("Payload Nível 1:", payload_nivel_1["nivelAbaixo"])
    
    # Criar payload com nível 2 (detalhado)
    payload_nivel_2 = criar_payload_geral(
        entidade, componente, etapa, ciclo,
        installation_id, session_token, nivel_agregacao=2
    )
    print("Payload Nível 2:", payload_nivel_2["nivelAbaixo"])

# --------------------------------------------------------------------------
# COMPARAÇÃO DOS NÍVEIS
# --------------------------------------------------------------------------

def comparar_niveis():
    """Compara as configurações dos diferentes níveis"""
    from config_api import config_nivel
    
    print("=== COMPARAÇÃO DOS NÍVEIS DE AGREGAÇÃO ===\n")
    
    for nivel in [0, 1, 2]:
        config = config_nivel.get_config_nivel(nivel)
        print(f"Nível {nivel}:")
        print(f"  - nivelAbaixo: {config['nivelAbaixo']}")
        print(f"  - Descrição: {config['descricao']}")
        print()

# --------------------------------------------------------------------------
# EXEMPLO DE USO PRÁTICO
# --------------------------------------------------------------------------

def exemplo_uso_pratico():
    """Exemplo prático de como usar os diferentes níveis"""
    
    print("=== EXEMPLO DE USO PRÁTICO ===\n")
    
    # Cenário 1: Análise rápida (nível 0)
    print("1. Análise Rápida (Nível 0):")
    print("   - Use para obter visão geral dos dados")
    print("   - Carregamento mais rápido")
    print("   - Ideal para dashboards executivos")
    print()
    
    # Cenário 2: Análise detalhada (nível 1)
    print("2. Análise Detalhada (Nível 1):")
    print("   - Use para análises intermediárias")
    print("   - Equilíbrio entre informação e performance")
    print("   - Ideal para análises pedagógicas")
    print()
    
    # Cenário 3: Análise granular (nível 2)
    print("3. Análise Granular (Nível 2):")
    print("   - Use para análises profundas")
    print("   - Máximo detalhamento disponível")
    print("   - Ideal para pesquisas e estudos específicos")
    print()

# --------------------------------------------------------------------------
# INSTRUÇÕES DE USO
# --------------------------------------------------------------------------

def instrucoes_uso():
    """Instruções de como usar a modularização"""
    
    print("=== INSTRUÇÕES DE USO ===\n")
    
    print("Para alterar o nível de agregação:")
    print()
    print("1. ALTERAÇÃO SIMPLES (Recomendada):")
    print("   - Abra o arquivo config_api.py")
    print("   - Altere a linha: NIVEL_PADRAO = 0")
    print("   - Substitua 0 por 1 ou 2 conforme desejado")
    print("   - Salve o arquivo e reinicie a aplicação")
    print()
    
    print("2. ALTERAÇÃO VIA INTERFACE:")
    print("   - Execute a aplicação")
    print("   - Use o seletor na sidebar 'Nível de Agregação dos Dados'")
    print("   - Escolha entre os níveis 0, 1 ou 2")
    print("   - Os dados serão recarregados automaticamente")
    print()
    
    print("3. ALTERAÇÃO PROGRAMÁTICA:")
    print("   - Use as funções do módulo nivel_config.py")
    print("   - Exemplo: definir_nivel(1)")
    print("   - Útil para lógica condicional baseada em critérios")
    print()

if __name__ == "__main__":
    print("=== DEMONSTRAÇÃO DA MODULARIZAÇÃO ===\n")
    
    # Executar exemplos
    comparar_niveis()
    exemplo_uso_pratico()
    instrucoes_uso()
    
    # Executar exemplos práticos (descomente para testar)
    # exemplo_alteracao_programatica()
    # exemplo_niveis_especificos()
