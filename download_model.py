import subprocess

subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
