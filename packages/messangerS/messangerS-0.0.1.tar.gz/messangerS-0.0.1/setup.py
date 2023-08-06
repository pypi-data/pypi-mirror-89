from setuptools import setup, find_packages

setup(name="messangerS",
      version="0.0.1",
      description="messangerS",
      author="GalAR",
      author_email="galina_87@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
