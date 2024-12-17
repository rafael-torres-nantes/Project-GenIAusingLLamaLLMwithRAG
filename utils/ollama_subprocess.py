import subprocess
from time import sleep

def start_ollama():
    try:
        subprocess.run(["ollama", "run", "llama3.2"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Ollama processes started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while starting Ollama processes: {e}")

def stop_ollama():
    try:
        subprocess.run(["ollama", "stop", "llama3.2"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ollama", "stop", "nomic-embed-text"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Ollama processes stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while stopping Ollama processes: {e}")

if __name__ == "__main__":
    start_ollama()
    # subprocess.run(["ollama", "ps"], check=True)
    # stop_ollama()
    # subprocess.run(["ollama", "ps"], check=True)