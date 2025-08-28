# Challenge---Sprint-3---Python

## Otimização do Controle de Insumos com Estruturas de Dados

### 🎯 Visão Geral do Projeto

Este projeto apresenta uma solução computacional para o desafio de baixa visibilidade no apontamento de consumo de insumos (reagentes, descartáveis, etc.) em unidades de diagnóstico. O processo manual de registro atual gera atrasos e imprecisões, resultando em discrepâncias de estoque, custos elevados e ineficiência operacional.

Utilizando estruturas de dados e algoritmos clássicos em Python, este sistema simula o registro de consumo e implementa funcionalidades para organizar e consultar os dados de forma eficiente, transformando um processo falho em um sistema de gestão inteligente e orientado por dados.

### ✨ Funcionalidades Implementadas

O script principal (`main.py`, por exemplo) simula e gerencia os dados de consumo, aplicando diferentes técnicas para cada necessidade específica.

#### 1. Fila (Queue) - Registro Cronológico

* **Problema:** Garantir que os consumos sejam processados na ordem exata em que ocorreram (FIFO - First-In, First-Out).
* **Solução:** Uma Fila foi implementada para enfileirar cada novo consumo. O sistema de baixa de estoque processa os itens do início da fila, garantindo a integridade cronológica.
* **Benefício:** Reflete o fluxo real de uso dos materiais e elimina discrepâncias no estoque.

```python
from collections import deque

class FilaConsumo:
    def __init__(self):
        self.fila = deque()

    def registrar_consumo(self, registro):
        """Adiciona um novo consumo ao final da fila."""
        self.fila.append(registro)

    def processar_proximo_consumo(self):
        """Processa o consumo mais antigo (início da fila)."""
        if not self.fila:
            return None
        return self.fila.popleft()
```

#### 2. Pilha (Stack) - Consulta de Atividades Recentes

* **Problema**: Permitir a consulta rápida dos últimos lançamentos ou implementar uma função "desfazer".

* **Solução**: Uma Pilha (LIFO - Last-In, First-Out) armazena os registros. O último item a entrar é o primeiro a sair, ideal para visualizar a atividade mais recente.

* **Benefício**: Agiliza a verificação de atividades e a correção de erros de lançamento.


```python
class PilhaConsultaRecente:
    def __init__(self):
        self.pilha = []

    def adicionar_a_consulta(self, registro):
        self.pilha.append(registro)

    def desfazer_ultimo_lancamento(self):
        """Remove e retorna o último consumo da pilha."""
        if not self.pilha:
            return None
        return self.pilha.pop()
```

#### 3. Algoritmos de Busca - Localização de Insumos

* **Problema**: Encontrar rapidamente todos os registros de consumo de um item específico para auditoria ou análise de padrão de uso.

* **Solução**:
  * **Busca Sequencial**: Itera sobre toda a lista. Simples e eficaz para listas pequenas.
  * **Busca Binária**: Exige uma lista ordenada e é extremamente eficiente, dividindo o campo de busca pela metade a cada passo.

* **Benefício**: A Busca Binária oferece um ganho de performance imenso para sistemas com grande histórico de dados.


```python
# Busca Binária exige que a lista esteja ordenada pelo nome do insumo
def busca_binaria(lista_ordenada, nome_insumo):
    esquerda, direita = 0, len(lista_ordenada) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if lista_ordenada[meio]['insumo'] == nome_insumo:
            return lista_ordenada[meio]
        elif lista_ordenada[meio]['insumo'] < nome_insumo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return None
```


#### 4. Algoritmos de Ordenação - Geração de Relatórios Estratégicos

* **Problema**: Transformar dados brutos de consumo em insights acionáveis.

* **Solução**:
  * **Merge Sort**: Utilizado para ordenar os insumos por quantidade consumida, gerando relatórios de Curva ABC para identificar os itens de maior impacto.
  * **Quick Sort**: Utilizado para ordenar os insumos por data de validade, permitindo uma estratégia FEFO (First-Expire, First-Out) para reduzir o desperdício.

* **Benefício**: Converte dados em inteligência de negócio, apoiando a tomada de decisão para otimizar compras e reduzir perdas.


```python
# Quick Sort para ordenar por data de validade
def quick_sort(lista, chave='data_validade'):
    if len(lista) <= 1:
        return lista
    pivo = lista[len(lista) // 2][chave]
    menores = [x for x in lista if x[chave] < pivo]
    iguais = [x for x in lista if x[chave] == pivo]
    maiores = [x for x in lista if x[chave] > pivo]
    return quick_sort(menores, chave) + iguais + quick_sort(maiores, chave)
```


### 🚀 Como Executar
#### Pré-requisitos:

* Ter o Python 3 instalado.

 1. #### Clone o repositório:


  ```bash
  git clone [https://github.comGabrielGaleraniAlmeida/Challenge---Sprint-3---Python.git](https://github.com/GabrielGaleraniAlmeida/Challenge---Sprint-3---Python.git)
  cd seu-repositorio
  ```

 2. #### Execute o script:


  ```bash
  python nome_do_arquivo.py
  ```
  
O script irá simular os dados de consumo e imprimir no terminal as demonstrações de cada uma das funcionalidades implementadas.

### 📋 Exemplo de Saída


```plaintext
--- AMOSTRA DE DADOS SIMULADOS ---
{'insumo': 'Seringa 5ml', 'quantidade': 42, 'data_consumo': '2025-08-20', 'data_validade': '2026-07-10'}
...

--- 1. DEMONSTRAÇÃO DA FILA (FIFO) ---
✔️  REGISTRADO: Seringa 5ml (Qtd: 42)
✔️  REGISTRADO: Agulha Descartável (Qtd: 88)
Processando baixas no sistema...
⚙️  PROCESSANDO BAIXA: Seringa 5ml (Qtd: 42)
...

--- 4. DEMONSTRAÇÃO DE ORDENAÇÃO ---

Relatório de Itens Mais Consumidos (Ordenado com Merge Sort por Quantidade):
  - Reagente A: 99 unidades
  - Gaze Estéril: 98 unidades
  ...

Relatório de Itens com Validade Próxima (Ordenado com Quick Sort):
  - Luva de Procedimento (Par): Validade 2025-09-25
  - Agulha Descartável: Validade 2025-09-28
  ...
```
