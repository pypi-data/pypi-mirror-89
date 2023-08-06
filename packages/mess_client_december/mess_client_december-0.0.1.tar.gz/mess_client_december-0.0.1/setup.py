from setuptools import setup, find_packages

setup(name="mess_client_december",
      version="0.0.1",
      description="mess_client_december",
      author="Alex Morev",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
