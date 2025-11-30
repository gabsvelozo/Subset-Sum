import random
import time
import subprocess
import statistics
import tempfile
import json
from algoritmos.SubsetSum import subset_sum as ss_py


def generate_array(size):
    return [random.randint(1, size) for _ in range(size)]

def generate_target(size):
    return random.randint(1, size)

def generate_inputs():
    return {
        "pequeno": 25,
        "medio":5000,
        "grande": 500000
    }



def benchmark_python(size, target):
    tempos = []

    for _ in range(20):
        arr = generate_array(size)
        start = time.time()
        ss_py(arr, target)
        end = time.time()
        tempos.append((end - start) * 1000)

    return statistics.mean(tempos), statistics.stdev(tempos), tempos


def benchmark_java(size, target):
    tempos = []

    for _ in range(20):
        java_cmd = [
            "java", "-cp", ".", "algoritmos.SubsetSum",
            str(size),
            str(target)
        ]

        start = time.time()
        subprocess.run(java_cmd, stdout=subprocess.DEVNULL)
        end = time.time()

        tempos.append(end - start)

    media = sum(tempos) / len(tempos)
    std = statistics.pstdev(tempos)

    return media, std, tempos


def run_all():
    entradas = generate_inputs()

    for nome, size in entradas.items():
        target = generate_target(size)

        print(f"\n===== {nome.upper()} =====")
        print(f"Tamanho: {size}, Target: {target}")

        media_py, std_py, tempos_py = benchmark_python(size, target)
        print(f"Python -> média: {media_py:.4f} ms | desvio: {std_py:.4f} ms")

        media_java, std_java, tempos_java = benchmark_java(size, target)
        print(f"Java   -> média: {media_java:.4f} ms | desvio: {std_java:.4f} ms")


if __name__ == "__main__":
    run_all()

