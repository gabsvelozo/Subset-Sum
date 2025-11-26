# Projeto: Subset Sum (Soma de Subconjuntos)
**Disciplina:** Teoria da Computação | **Instituição:** CESAR School

Este repositório contém a implementação e análise de complexidade do algoritmo **Subset Sum** (Soma de Subconjuntos), desenvolvido em **Python** e **Java** para fins de comparação de desempenho.

---

## 1. O Que é o Problema?

### Explicação Intuitiva (Analogia do Troco)
Imagine que você tem algumas notas de dinheiro no bolso (ex: R$ 2, R$ 5, R$ 10) e quer saber se consegue pagar uma conta de exatamente R$ 7 sem precisar de troco.
- **Entrada:** Suas notas `[2, 5, 10]` e o alvo `7`.
- **Lógica:** Testar combinações. A nota de 2 sozinha não dá. A de 5 sozinha não dá. Mas `2 + 5 = 7`.
- **Saída:** `Verdadeiro` (Sim, é possível).

### Definição Formal
Dado um conjunto de números inteiros não-negativos e um valor alvo (*target*), o objetivo é determinar se existe algum subconjunto desses números cuja soma seja exatamente igual ao alvo.

---

## 2. Como Resolvemos (O Algoritmo)

Utilizamos a técnica de **Programação Dinâmica**. Em vez de força bruta (testar todas as combinações, o que seria muito lento), criamos uma "tabela de verdades".

### Lógica Implementada
1. Criamos um vetor booleano `dp` de tamanho `target + 1`.
2. A posição `dp[i]` indica se a soma `i` é possível.
3. Começamos com `dp[0] = True` (soma zero é sempre possível: basta não escolher nada).
4. Para cada número `x` da nossa lista, percorremos o vetor `dp`. Se a soma `j - x` já era possível antes, então a soma `j` agora também é possível.

### Pseudocódigo
```text
Função SubsetSum(arr, target):
    Criar vetor dp[target + 1] inicializado como Falso
    dp[0] = Verdadeiro

    Para cada numero x em arr:
        Para j de target até x (decrescente):
            dp[j] = dp[j] OU dp[j - x]
    
    Retornar dp[target]
```
## 3. Análise de Complexidade

A eficiência deste algoritmo depende não apenas da quantidade de números, mas também do valor da soma alvo (*target*).

### ⏱️ Complexidade de Tempo
Nossa implementação percorre todos os números e, para cada um, atualiza a tabela até o valor do *target*. Como não há interrupções antecipadas no código, o comportamento é consistente:

- **Pior Caso (Big-O):** $O(N \cdot S)$
- **Melhor Caso (Big-Ω):** $\Omega(N \cdot S)$
- **Caso Médio (Big-Θ):** $\Theta(N \cdot S)$

> **Onde:**
> - $N$ = Quantidade de elementos no conjunto.
> - $S$ = Valor da soma alvo (*target*).

### 💾 Complexidade de Espaço
Utilizamos um vetor unidimensional para armazenar os resultados parciais.
- **Espaço:** $O(S)$ (Proporcional ao valor do *target*).

### 🧠 Classificação do Problema (P vs NP)
O problema *Subset Sum* é classicamente **NP-Completo**.
- **Isso significa que:** Não se conhece um algoritmo que o resolva em tempo puramente polinomial ($O(N^k)$) para qualquer entrada.
- **Sobre nossa solução:** Ela é considerada **Pseudo-Polinomial**. Ela é rápida para *targets* pequenos, mas se o *target* for um número gigantesco (exponencial em relação ao número de bits), o algoritmo se torna inviável.

---

## 4. Discussão sobre a Aplicabilidade Prática

Este algoritmo é eficiente quando o valor da soma alvo ($S$) e o número de elementos ($N$) são pequenos ou moderados.

### ✅ Contextos Favoráveis
- **Problemas de Troco:** Verificar se é possível dar um troco exato com as moedas disponíveis.
- **Particionamento de Conjuntos:** Dividir recursos ou tarefas de valores baixos de forma equitativa.
- **Transações Financeiras Simples:** Conciliação bancária onde se busca quais transações somam um valor específico.

### ❌ Contextos Ineficientes
Se o alvo $S$ for muito grande (ex: $10^9$), o vetor `dp` consumirá muita memória e o tempo de execução será proibitivo, mesmo que $N$ seja pequeno. Isso ocorre porque a complexidade depende do valor numérico, tornando-o um algoritmo de tempo **pseudo-polinomial**.

## 5. Análise de Casos (Melhor, Pior e Médio)

A performance do algoritmo varia pouco devido à natureza da implementação baseada em preenchimento completo da tabela.

- **Pior Caso:** $O(N \cdot S)$
  - Ocorre quando precisamos preencher toda a tabela, o que é o padrão nesta implementação (sem otimizações de parada antecipada).
- **Melhor Caso:** $O(N \cdot S)$
  - Teoricamente, seria possível parar assim que `dp[target]` se tornasse `True`. No entanto, na implementação atual (tanto Java quanto Python), o laço percorre todos os itens para preencher a matriz. Portanto, o tempo de execução é consistente e previsível, sem variação significativa baseada na ordem dos dados.
- **Caso Médio:** $O(N \cdot S)$
  - Segue a mesma lógica, pois a estrutura dos laços é fixa e independente da sorte na distribuição dos números.

---

## 6. Reflexão Final (Classe P vs NP)

O problema **Subset Sum** pertence à classe **NP-Completo**.

### ❓ É classe P?
**Não se sabe.**
Se $P \neq NP$ (a conjectura mais aceita na ciência da computação), então não existe algoritmo que resolva este problema em tempo polinomial em relação ao *tamanho da entrada* (número de bits).

### 🚀 Por que a solução parece rápida?
A solução apresentada é **Pseudo-Polinomial**.
- Ela é polinomial em relação ao *valor* da soma ($S$).
- Porém, é exponencial em relação ao *número de bits* necessários para representar $S$. Se dobrarmos o número de bits do target (por exemplo, de 1 milhão para 1 trilhão), o tempo de execução aumenta drasticamente, tornando-a inviável para números muito grandes.

### 🔗 Contexto Teórico
- **Versão NP:** A versão de decisão ("existe um subconjunto?") é a que define a classe NP-Completo.
- **Problemas Semelhantes:**
  - **Problema da Mochila (Knapsack Problem):** Maximização de valor com limite de peso.
  - **Problema da Partição (Partition Problem):** Dividir um conjunto em dois com mesma soma.
  - Ambos também são NP-completos e frequentemente resolvidos com técnicas similares de Programação Dinâmica.
