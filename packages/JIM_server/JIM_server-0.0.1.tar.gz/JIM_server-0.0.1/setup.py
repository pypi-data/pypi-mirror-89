from setuptools import setup, find_packages

setup(name="JIM_server",
      version="0.0.1",
      description="messegers server",
      author="Firdos Aliev",
      author_email="firdos1234567891@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
