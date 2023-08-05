Struktura folderów 

pakiet_Mariusza
├── LICENSE
├── README.md
├── example_pkg
│	├──moj_modul1.py
│	├──moj_modul2.py
│   └── __init__.py
└── setup.py

Procedura tworzenia pakietu
1. Utwórz pliki o strukturze jak powyżej
2. w pliku setup.py dodaj kod:

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'nazwa_pakietu'
AUTHOR ='Ty'
AUTHOR_EMAIL = 'mail'
URL = 'Twój github'

LICENSE = 'MIT'
DESCRIPTION = 'Kilka przydatnych funkcji zwracających czas w różnych postaciach'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = []

setup(name=PACKAGE_NAME,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
)

3. Wypełnij swoje moduły kodem
4. Sprawdz czy pakiet działa odwołując się do niego z innego pliku (poza pakietem)
5. zainstaluj twine     pip install twine
6. zbuduj instalatora   python setup.py sdist bdist_wheel
7. sprawdź builda       twine check dist/*
8. opublikuj pakiet     twine upload dist/*
9. podczas publikacji jako użytkownika podaj __token__
10. Hasło jest = wartości tokena