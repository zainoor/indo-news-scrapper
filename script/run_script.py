import subprocess
from concurrent.futures import ThreadPoolExecutor

scripts = [
    "script_scrapper/detik.py",
    "script_scrapper/kompas.py",
    "script_scrapper/tempo.py",
    "script_scrapper/cnn.py"
]

def run_script(script):
    print(f"🚀 Running {script}")
    subprocess.run(["python", script])

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.map(run_script, scripts)
