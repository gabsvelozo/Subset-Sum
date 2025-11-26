import random
import time
import subprocess
import statistics
import tempfile
import json
from algoritmos.SubsetSum import subset_sum as ss_py


def generate_array(size):
    return [random.randint(1, 50) for _ in range(size)]

def generate_target(arr):
    return random.randint(1, len(arr))

def generate_inputs():
    return {
        "pequeno": generate_array(25),
        "medio": generate_array(5000),
        "grande": generate_array(1000000)
    }



def benchmark_python(arr, target):
    tempos = []

    for _ in range(20):
        start = time.time()
        ss_py(arr, target)
        end = time.time()
        tempos.append((end - start) * 1000)

    return statistics.mean(tempos), statistics.stdev(tempos), tempos


def benchmark_java(arr, target):
    tempos = []

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as f:
        json.dump(arr, f)
        arr_path = f.name

    for _ in range(20):
        start = time.time()
        java_cmd = [
            "java", "-cp", ".", "algoritmos.SubsetSum",
            str(target),
            arr_path
        ]
        subprocess.run(java_cmd, stdout=subprocess.DEVNULL)
        tempos.append(time.time() - start)

    media = sum(tempos) / len(tempos)
    std = statistics.pstdev(tempos)

    return media, std, tempos


def run_all():
    entradas = generate_inputs()

    for nome, arr in entradas.items():
        target = generate_target(arr)

        print(f"\n===== {nome.upper()} =====")
        print(f"Tamanho: {len(arr)}, Target: {target}")

        media_py, std_py, tempos_py = benchmark_python(arr, target)
        print(f"Python -> média: {media_py:.4f} ms | desvio: {std_py:.4f} ms")

        media_java, std_java, tempos_java = benchmark_java(arr, target)
        print(f"Java   -> média: {media_java:.4f} ms | desvio: {std_java:.4f} ms")


if __name__ == "__main__":
    run_all()

