from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='project',                                
    version="0.0.1",
    description="Conta_tu_to_conto",
    install_requires=requirements,
    packages=find_packages(),
    zip_safe=False)
