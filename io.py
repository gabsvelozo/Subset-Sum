import random
import time
import subprocess
import statistics
import tempfile
import json
import matplotlib.pyplot as plt  # Importação nova para os gráficos
from algoritmos.SubsetSum import subset_sum as ss_py

# --- CONFIGURAÇÃO DAS ENTRADAS ---
def generate_array(size):
    # Valores aleatórios entre 1 e 50
    return [random.randint(1, 50) for _ in range(size)]

def generate_target(arr):
    # Target aleatório (proporcional ao tamanho da lista)
    return random.randint(1, len(arr) * 10)

def generate_inputs():
    return {
        "pequeno": generate_array(25),      # N = 25
        "medio": generate_array(2000),      # N = 2.000
        "grande": generate_array(10000)     # N = 10.000 (Reduzido para não travar!)
    }

# --- FUNÇÕES DE BENCHMARK ---
def benchmark_python(arr, target):
    tempos = []
    # Executa 15 vezes (dentro do pedido de 15 a 30)
    for _ in range(15):
        start = time.time()
        ss_py(arr, target)
        end = time.time()
        tempos.append((end - start) * 1000) # Converte para ms

    return statistics.mean(tempos), statistics.stdev(tempos)

def benchmark_java(arr, target):
    tempos = []
    # Cria arquivo temporário para passar dados ao Java
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as f:
        json.dump(arr, f)
        arr_path = f.name

    for _ in range(15):
        start = time.time()
        java_cmd = [
            "java", "-cp", ".", "algoritmos.SubsetSum",
            str(target),
            arr_path
        ]
        subprocess.run(java_cmd, stdout=subprocess.DEVNULL)
        tempos.append((time.time() - start) * 1000) # Converte para ms

    return statistics.mean(tempos), statistics.stdev(tempos)

# --- FUNÇÃO DE PLOTAGEM (NOVA) ---
def plot_results(resultados):
    labels = list(resultados.keys()) # ['pequeno', 'medio', 'grande']
    py_means = [resultados[k]['python'] for k in labels]
    java_means = [resultados[k]['java'] for k in labels]

    x = range(len(labels))  # Localização das barras no eixo X
    width = 0.35            # Largura das barras

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Criando as barras
    rects1 = ax.bar([i - width/2 for i in x], py_means, width, label='Python', color='#3776ab')
    rects2 = ax.bar([i + width/2 for i in x], java_means, width, label='Java', color='#f89820')

    # Textos e Legendas
    ax.set_ylabel('Tempo Médio (ms)')
    ax.set_title('Comparação de Desempenho: Python vs Java (Subset Sum)')
    ax.set_xticks(x)
    ax.set_xticklabels([l.upper() for l in labels])
    ax.legend()

    # Adicionando o valor em cima de cada barra
    ax.bar_label(rects1, padding=3, fmt='%.1f')
    ax.bar_label(rects2, padding=3, fmt='%.1f')

    # Ajuste de layout e salvamento
    fig.tight_layout()
    plt.savefig('comparacao_tempos.png')
    print("\n✅ Gráfico gerado com sucesso: 'comparacao_tempos.png'")

# --- EXECUÇÃO PRINCIPAL ---
def run_all():
    entradas = generate_inputs()
    resultados_para_plot = {}

    print("Iniciando Benchmarks... (Isso pode levar alguns segundos)")

    for nome, arr in entradas.items():
        target = generate_target(arr)
        print(f"\n===== {nome.upper()} (N={len(arr)}) =====")

        # Roda Python
        media_py, std_py = benchmark_python(arr, target)
        print(f"Python: {media_py:.2f} ms (±{std_py:.2f})")

        # Roda Java
        media_java, std_java = benchmark_java(arr, target)
        print(f"Java:   {media_java:.2f} ms (±{std_java:.2f})")
        
        # Salva dados para o gráfico
        resultados_para_plot[nome] = {
            'python': media_py,
            'java': media_java
        }

    # Gera o gráfico no final
    plot_results(resultados_para_plot)

if __name__ == "__main__":
    run_all()