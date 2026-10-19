from setuptools import setup
import subprocess


version = subprocess.run(
    "git describe --tags --match [0-9]*.[0-9]*.[0-9]*".split(),
    stdout=subprocess.PIPE
).stdout.decode('utf-8').strip()

try:
    setup(version=version)
except Exception as e:
    if e.args[0].startswith("Invalid version: "):
        setup(version='0.0.0')
    else:
        print(e)
