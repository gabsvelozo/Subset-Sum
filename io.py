import random
import time
import subprocess
import statistics
import tempfile
import json
import matplotlib.pyplot as plt
import numpy as np
from algoritmos.SubsetSum import subset_sum as ss_py

# --- CONFIGURAÇÃO DAS ENTRADAS ---
def generate_array(size):
    return [random.randint(1, 50) for _ in range(size)]

def generate_target(arr):
    # O target é proporcional ao tamanho (média 5 * N)
    return random.randint(1, len(arr) * 10)

def generate_inputs():
    # Mantivemos o tamanho 10.000 para não travar, mas é suficiente para a curva
    return {
        "pequeno": generate_array(25),      # N = 25
        "medio": generate_array(2000),      # N = 2.000
        "grande": generate_array(10000)     # N = 10.000
    }

# --- BENCHMARKS ---
def benchmark_python(arr, target):
    tempos = []
    for _ in range(15):
        start = time.time()
        ss_py(arr, target)
        end = time.time()
        tempos.append((end - start) * 1000)
    return statistics.mean(tempos), statistics.stdev(tempos)

def benchmark_java(arr, target):
    tempos = []
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as f:
        json.dump(arr, f)
        arr_path = f.name

    for _ in range(15):
        start = time.time()
        java_cmd = ["java", "-cp", ".", "algoritmos.SubsetSum", str(target), arr_path]
        subprocess.run(java_cmd, stdout=subprocess.DEVNULL)
        tempos.append((time.time() - start) * 1000)
    return statistics.mean(tempos), statistics.stdev(tempos)

# --- GRÁFICO 1: BARRAS (COMPARATIVO) ---
def plot_bars(resultados):
    labels = list(resultados.keys())
    py_vals = [resultados[k]['python']['mean'] for k in labels]
    java_vals = [resultados[k]['java']['mean'] for k in labels]
    py_std = [resultados[k]['python']['std'] for k in labels]
    java_std = [resultados[k]['java']['std'] for k in labels]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    r1 = ax.bar(x - width/2, py_vals, width, label='Python (NumPy)', yerr=py_std, capsize=5, color='#3776ab')
    r2 = ax.bar(x + width/2, java_vals, width, label='Java', yerr=java_std, capsize=5, color='#f89820')

    ax.set_ylabel('Tempo (ms)')
    ax.set_title('Python vs Java: Comparação Direta')
    ax.set_xticks(x)
    ax.set_xticklabels([l.upper() for l in labels])
    ax.legend()
    
    ax.bar_label(r1, padding=3, fmt='%.1f')
    ax.bar_label(r2, padding=3, fmt='%.1f')
    
    plt.tight_layout()
    plt.savefig('comparacao_tempos.png')
    print("✅ Gráfico de Barras salvo: 'comparacao_tempos.png'")
    plt.close()

# --- GRÁFICO 2: CURVA TEÓRICA VS PRÁTICA (NOVO!) ---
def plot_curves(dados_para_curva):
    # Organiza os dados pelo tamanho N (x)
    dados_sorted = sorted(dados_para_curva, key=lambda x: x['n'])
    
    N = np.array([d['n'] for d in dados_sorted])
    Target = np.array([d['target'] for d in dados_sorted])
    Times_Py = np.array([d['time_py'] for d in dados_sorted])
    Times_Java = np.array([d['time_java'] for d in dados_sorted])

    # A "Complexidade Teórica" é proporcional a N * Target (ou N^2 neste teste)
    # Calculamos a "Carga de Trabalho" teórica
    Ops = N * Target 
    
    # Normalização: Ajustamos a curva teórica para "encostar" no último ponto medido do Java
    # Isso serve para ver se o formato da curva bate, não o valor absoluto.
    fator_escala = Times_Java[-1] / Ops[-1]
    Curva_Teorica = Ops * fator_escala

    plt.figure(figsize=(10, 6))
    
    # Plota as linhas medidas
    plt.plot(N, Times_Java, 'o-', label='Medido: Java', color='#f89820', linewidth=2)
    plt.plot(N, Times_Py, 'o-', label='Medido: Python', color='#3776ab', linewidth=2)
    
    # Plota a Curva Teórica (Pontilhada)
    # Usamos N no eixo X para visualizar o crescimento quadrático
    plt.plot(N, Curva_Teorica, '--', label='Teórico O(N*S)', color='gray', alpha=0.7)

    plt.xlabel('Tamanho da Entrada (N)')
    plt.ylabel('Tempo de Execução (ms)')
    plt.title('Curva de Complexidade: Teoria vs Prática')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('curva_complexidade.png')
    print("✅ Gráfico de Curvas salvo: 'curva_complexidade.png'")
    plt.close()

# --- EXECUÇÃO ---
def run_all():
    entradas = generate_inputs()
    resultados = {}
    dados_curva = []

    print("Iniciando Benchmarks...")

    for nome, arr in entradas.items():
        target = generate_target(arr)
        n = len(arr)
        print(f"\n--- {nome.upper()} (N={n}, Target={target}) ---")

        # Benchmarks
        mean_py, std_py = benchmark_python(arr, target)
        mean_java, std_java = benchmark_java(arr, target)
        
        print(f"Python: {mean_py:.2f} ms")
        print(f"Java:   {mean_java:.2f} ms")

        # Guarda dados para o Gráfico de Barras
        resultados[nome] = {
            'python': {'mean': mean_py, 'std': std_py},
            'java': {'mean': mean_java, 'std': std_java}
        }
        
        # Guarda dados para o Gráfico de Curvas
        dados_curva.append({
            'n': n,
            'target': target,
            'time_py': mean_py,
            'time_java': mean_java
        })

    plot_bars(resultados)
    plot_curves(dados_curva)

if __name__ == "__main__":
    run_all()