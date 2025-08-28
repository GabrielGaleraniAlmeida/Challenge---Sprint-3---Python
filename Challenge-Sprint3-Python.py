# -*- coding: utf-8 -*-
"""
Relatório Técnico: Solução para Controle de Consumo de Insumos.
Este script implementa estruturas de dados e algoritmos clássicos para
resolver o desafio de baixa visibilidade no apontamento de consumo em
unidades de diagnóstico.
"""
import datetime
import random
from collections import deque


# --------------------------------------------------------------------------
# 1. SIMULAÇÃO DE DADOS
# --------------------------------------------------------------------------
def simular_dados_consumo(dias=5):
    """
    Simula o consumo diário de insumos em uma unidade de diagnóstico.
    """
    insumos_base = [
        "Seringa 5ml", "Agulha Descartável", "Luva de Procedimento (Par)",
        "Reagente A", "Reagente B", "Tubo de Coleta (EDTA)", "Gaze Estéril"
    ]
    dados_consumo = []
    data_inicial = datetime.date(2025, 8, 20)

    # Simula vários consumos ao longo dos dias
    for i in range(dias * len(insumos_base)):
        data_consumo = data_inicial + datetime.timedelta(days=random.randint(0, dias - 1))
        insumo = random.choice(insumos_base)
        quantidade = random.randint(1, 100)
        validade = data_consumo + datetime.timedelta(days=random.randint(30, 365))

        dados_consumo.append({
            "insumo": insumo,
            "quantidade": quantidade,
            "data_consumo": data_consumo.strftime("%Y-%m-%d"),
            "data_validade": validade.strftime("%Y-%m-%d")
        })

    # Garante que os dados estejam em ordem cronológica para a simulação da fila
    dados_consumo.sort(key=lambda x: x['data_consumo'])
    return dados_consumo


# --------------------------------------------------------------------------
# 2. IMPLEMENTAÇÃO DE FILA E PILHA
# --------------------------------------------------------------------------
class FilaConsumo:
    """Gerencia o registro de consumo em ordem cronológica (FIFO)."""

    def __init__(self):
        self.fila = deque()

    def registrar_consumo(self, registro):
        print(f"✔️  REGISTRADO: {registro['insumo']} (Qtd: {registro['quantidade']})")
        self.fila.append(registro)

    def processar_proximo_consumo(self):
        if not self.fila:
            print("⚠️  Fila de consumo vazia.")
            return None
        registro_processado = self.fila.popleft()
        print(f"⚙️  PROCESSANDO BAIXA: {registro_processado['insumo']} (Qtd: {registro_processado['quantidade']})")
        return registro_processado


class PilhaConsultaRecente:
    """Gerencia consultas em ordem inversa (LIFO), para ver os últimos registros."""

    def __init__(self):
        self.pilha = []

    def adicionar_a_consulta(self, registro):
        self.pilha.append(registro)

    def ver_ultimo_consumo(self):
        return self.pilha[-1] if self.pilha else "Pilha vazia."

    def desfazer_ultimo_lancamento(self):
        if not self.pilha:
            print("⚠️  Pilha vazia. Nada a desfazer.")
            return None
        ultimo = self.pilha.pop()
        print(f"⏪ DESFEITO: Lançamento de {ultimo['insumo']} (Qtd: {ultimo['quantidade']})")
        return ultimo


# --------------------------------------------------------------------------
# 3. IMPLEMENTAÇÃO DOS ALGORITMOS DE BUSCA
# --------------------------------------------------------------------------
def busca_sequencial(lista, nome_insumo):
    """Encontra todos os registros de um insumo específico."""
    encontrados = [reg for reg in lista if reg['insumo'] == nome_insumo]
    return encontrados


def busca_binaria(lista_ordenada, nome_insumo):
    """Encontra um registro de um insumo em uma lista JÁ ORDENADA."""
    esquerda, direita = 0, len(lista_ordenada) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        insumo_meio = lista_ordenada[meio]['insumo']
        if insumo_meio == nome_insumo:
            return lista_ordenada[meio]
        elif insumo_meio < nome_insumo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return None


# --------------------------------------------------------------------------
# 4. IMPLEMENTAÇÃO DOS ALGORITMOS DE ORDENAÇÃO
# --------------------------------------------------------------------------
def merge_sort(lista, chave='quantidade'):
    """Ordena a lista usando o algoritmo Merge Sort."""
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    metade_esquerda = merge_sort(lista[:meio], chave)
    metade_direita = merge_sort(lista[meio:], chave)

    # Função auxiliar 'merge'
    resultado = []
    i = j = 0
    while i < len(metade_esquerda) and j < len(metade_direita):
        if metade_esquerda[i][chave] <= metade_direita[j][chave]:
            resultado.append(metade_esquerda[i])
            i += 1
        else:
            resultado.append(metade_direita[j])
            j += 1
    resultado.extend(metade_esquerda[i:])
    resultado.extend(metade_direita[j:])
    return resultado


def quick_sort(lista, chave='data_validade'):
    """Ordena a lista usando o algoritmo Quick Sort."""
    if len(lista) <= 1:
        return lista
    pivo = lista[len(lista) // 2][chave]
    menores = [x for x in lista if x[chave] < pivo]
    iguais = [x for x in lista if x[chave] == pivo]
    maiores = [x for x in lista if x[chave] > pivo]
    return quick_sort(menores, chave) + iguais + quick_sort(maiores, chave)


# --------------------------------------------------------------------------
# 5. EXECUÇÃO E DEMONSTRAÇÃO
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # Gerar dados simulados para 10 dias
    dados = simular_dados_consumo(10)
    print("--- AMOSTRA DE DADOS SIMULADOS ---")
    for registro in dados[:3]:
        print(registro)

    print("\n\n--- 1. DEMONSTRAÇÃO DA FILA (FIFO) ---")
    fila_de_consumo = FilaConsumo()
    for registro in dados[:3]:
        fila_de_consumo.registrar_consumo(registro)
    print("\nProcessando baixas no sistema...")
    fila_de_consumo.processar_proximo_consumo()
    fila_de_consumo.processar_proximo_consumo()

    print("\n\n--- 2. DEMONSTRAÇÃO DA PILHA (LIFO) ---")
    pilha_de_consulta = PilhaConsultaRecente()
    for registro in dados[:4]:
        pilha_de_consulta.adicionar_a_consulta(registro)
    print("Último consumo registrado:", pilha_de_consulta.ver_ultimo_consumo())
    pilha_de_consulta.desfazer_ultimo_lancamento()
    print("Último consumo após desfazer:", pilha_de_consulta.ver_ultimo_consumo())

    print("\n\n--- 3. DEMONSTRAÇÃO DE BUSCAS ---")
    print("\nBuscando por 'Reagente A' (Busca Sequencial)...")
    registros_encontrados_seq = busca_sequencial(dados, "Reagente A")
    print(f"Resultados: {len(registros_encontrados_seq)} registros encontrados.")

    # Para a busca binária, a lista precisa estar ordenada pelo critério de busca
    dados_ordenados_por_nome = sorted(dados, key=lambda x: x['insumo'])
    print("\nBuscando por 'Seringa 5ml' (Busca Binária)...")
    resultado_binario = busca_binaria(dados_ordenados_por_nome, "Seringa 5ml")
    if resultado_binario:
        print(f"Resultado: Insumo '{resultado_binario['insumo']}' encontrado com sucesso.")
    else:
        print("Resultado: Insumo não encontrado.")

    print("\n\n--- 4. DEMONSTRAÇÃO DE ORDENAÇÃO ---")
    print("\nRelatório de Itens Mais Consumidos (Ordenado com Merge Sort por Quantidade):")
    # Invertemos a lista para ter a ordem decrescente
    ordenados_por_qtd_desc = merge_sort(dados, 'quantidade')[::-1]
    for item in ordenados_por_qtd_desc[:5]:
        print(f"  - {item['insumo']}: {item['quantidade']} unidades")

    print("\nRelatório de Itens com Validade Próxima (Ordenado com Quick Sort):")
    ordenados_por_validade = quick_sort(dados, 'data_validade')
    for item in ordenados_por_validade[:5]:
        print(f"  - {item['insumo']}: Validade {item['data_validade']}")