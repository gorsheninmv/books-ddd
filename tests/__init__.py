import subprocess

def run_integration_tests():
    subprocess.run(['python', '-u', '-m', 'unittest', 'discover', '-p', 'integration.py'])

def run_e2e_tests():
    subprocess.run(['python', '-u', '-m', 'unittest', 'discover', '-p', 'e2e.py'])
