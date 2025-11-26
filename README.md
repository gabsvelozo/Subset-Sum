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
