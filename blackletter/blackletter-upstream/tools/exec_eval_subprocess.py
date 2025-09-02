import subprocess
import sys

cmd = [sys.executable, 'rag/eval/evaluate.py', '--k', '5']
print('Running:', cmd)
proc = subprocess.run(cmd, capture_output=True, text=True)
print('Return code:', proc.returncode)
print('STDOUT:\n', proc.stdout)
print('STDERR:\n', proc.stderr)
