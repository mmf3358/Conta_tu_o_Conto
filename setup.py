from pathlib import Path
from setuptools import find_packages, setup

root = Path(__file__).resolve().parent
setup(name='conta-tu-o-conto', version='0.1.0',
      description='Interactive storytelling prototype with pretrained GPT-2',
      python_requires='>=3.10,<3.13',
      packages=find_packages(include=['project', 'project.*']),
      install_requires=(root / 'requirements.txt').read_text().splitlines(),
      package_data={'project': ['images/*.png']})
