from setuptools import setup, find_packages

setup(name="messangerC",
      version="0.0.1",
      description="messangerC",
      author="GalAR",
      author_email="galina_87@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )

