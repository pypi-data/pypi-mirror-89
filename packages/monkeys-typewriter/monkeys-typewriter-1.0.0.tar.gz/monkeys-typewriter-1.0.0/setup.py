from setuptools import setup, find_packages

setup(name='monkeys-typewriter',
      version=open('VERSION').read(),
      description="Monkey's Typewriter PEG parser",
      author='Adam Green',
      author_email='adam@tryal.ai',
      donwload_url='https://github.com/tryal-ai/mnkytw/archive/1.0.0.tar.gz',
      url='https://tryal.ai/',
      packages=find_packages(),
      keywords=["PEG", "parser", "grammar"],
      install_requires=[]
)