import time
import subprocess

while True:
    try:
        print("Menjalankan bot...")
        subprocess.run(["python", "belpin_bot.py"])
    except Exception as e:
        print(f"Terjadi error: {e}")
    print("Bot berhenti. Restart dalam 3 detik...")
    time.sleep(3)
