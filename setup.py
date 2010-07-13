from setuptools import setup

VERSION = "0.1b"

setup(name="gloss",
      version=VERSION,
      author="Bump Technologies, Inc.",
      author_email="dev@bumptechnologies.com",
      packages=["gloss"],
      entry_points={
          'console_scripts' : 
          ''' 
gloss=gloss.main:cli
'''
          },
    install_requires=[
    ],
)
