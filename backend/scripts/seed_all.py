import os
import subprocess
import sys

def run_seed(script_name):
    print(f"--- Running {script_name} ---")
    try:
        # On utilise sys.executable pour être sûr d'utiliser le même Python
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        subprocess.run([sys.executable, script_path], check=True)
        print(f"Successfully finished {script_name}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}\n")

if __name__ == "__main__":
    scripts = [
        "seed_users.py",
        "seed_templates.py",
        "seed_art_templates.py",
        "seed_ultimate_minimal.py",
        "seed_ora_template.py",
        "seed_extended_art_templates.py",
        "seed_premium_templates.py",
        "seed_ky_template.py",
        "seed_new_premium_templates.py"
    ]
    
    for script in scripts:
        run_seed(script)
    
    print("All seeds completed successfully!")
