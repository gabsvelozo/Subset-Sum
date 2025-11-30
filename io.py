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
    return random.randint(1, len(arr) * 10)

def generate_inputs():
    return {
        "pequeno": generate_array(25),
        "medio": generate_array(2000),
        "grande": generate_array(10000)
    }

# --- BENCHMARKS ---
def benchmark_python(arr, target):
    tempos = []
    for _ in range(15):
        start = time.time()
        ss_py(arr, target)
        end = time.time()
        tempos.append((end - start) * 1000)
    
    # Se houver apenas 1 item (erro raro), stdev quebra. Prevenção:
    if len(tempos) < 2: return statistics.mean(tempos), 0.0
    return statistics.mean(tempos), statistics.stdev(tempos)

def benchmark_java(arr, target):
    tempos = []
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as f:
        json.dump(arr, f)
        arr_path = f.name

    for _ in range(15):
        java_cmd = ["java", "-cp", ".", "algoritmos.SubsetSum", str(target), arr_path]
        
        # Captura o output do Java que agora imprime o tempo exato
        result = subprocess.run(java_cmd, capture_output=True, text=True)
        
        try:
            tempo_ms = float(result.stdout.strip())
            tempos.append(tempo_ms)
        except ValueError:
            print(f"Erro ao ler output do Java: {result.stderr}")
            tempos.append(0.0)
            
    if len(tempos) < 2: return statistics.mean(tempos), 0.0
    return statistics.mean(tempos), statistics.stdev(tempos)

# --- GRÁFICOS ---
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
    ax.set_title('Python vs Java: Comparação Direta (JVM Warmup Ignorado)')
    ax.set_xticks(x)
    ax.set_xticklabels([l.upper() for l in labels])
    ax.legend()
    
    # Adiciona os valores nas barras
    ax.bar_label(r1, padding=3, fmt='%.1f')
    ax.bar_label(r2, padding=3, fmt='%.1f')
    
    plt.tight_layout()
    plt.savefig('comparacao_tempos.png')
    print("✅ Gráfico de Barras salvo: 'comparacao_tempos.png'")
    plt.close()

def plot_curves(dados_para_curva):
    dados_sorted = sorted(dados_para_curva, key=lambda x: x['n'])
    
    N = np.array([d['n'] for d in dados_sorted])
    Target = np.array([d['target'] for d in dados_sorted])
    Times_Py = np.array([d['time_py'] for d in dados_sorted])
    Times_Java = np.array([d['time_java'] for d in dados_sorted])

    Ops = N * Target 
    
    # Ajuste da curva teórica para alinhar com o último ponto do Java
    fator_escala = Times_Java[-1] / Ops[-1] if Ops[-1] > 0 else 0
    Curva_Teorica = Ops * fator_escala

    plt.figure(figsize=(10, 6))
    
    plt.plot(N, Times_Java, 'o-', label='Medido: Java', color='#f89820', linewidth=2)
    plt.plot(N, Times_Py, 'o-', label='Medido: Python (NumPy)', color='#3776ab', linewidth=2)
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

# --- EXECUÇÃO PRINCIPAL ---
def run_all():
    entradas = generate_inputs()
    resultados = {}
    dados_curva = []

    print("Iniciando Benchmarks...")

    for nome, arr in entradas.items():
        target = generate_target(arr)
        n = len(arr)
        print(f"\n--- {nome.upper()} (N={n}, Target={target}) ---")

        mean_py, std_py = benchmark_python(arr, target)
        mean_java, std_java = benchmark_java(arr, target)
        
        # AQUI ESTAVA FALTANDO O DESVIO PADRÃO NO PRINT
        print(f"Python: {mean_py:.2f} ms (±{std_py:.2f})")
        print(f"Java:   {mean_java:.2f} ms (±{std_java:.2f})")

        resultados[nome] = {
            'python': {'mean': mean_py, 'std': std_py},
            'java': {'mean': mean_java, 'std': std_java}
        }
        
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