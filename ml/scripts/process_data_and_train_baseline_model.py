import sys
import subprocess


def run(module_name: str) -> None:
    subprocess.run([sys.executable, "-m", module_name], check=True)


if __name__ == "__main__":
    run("ml.processing.clean_transaction_data")
    run("ml.processing.split_data")
    run("ml.training.train_baseline")
