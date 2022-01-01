import subprocess

def run_integration_tests():
    subprocess.run(['python', '-u', '-m', 'unittest', 'discover', '-p', 'integration.py'])
