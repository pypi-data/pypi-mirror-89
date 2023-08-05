from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='sparsity-pattern',
      version='0.4.0',
      description=(
          "Generate different types of sparsity pattern for sparse matrices."
      ),
      # long_description=read('README.md'),
      # long_description_content_type='text/markdown',
      url='http://github.com/ulf1/sparsity-pattern',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['sparsity_pattern'],
      install_requires=[
          'setuptools>=40.0.0'],
      python_requires='>=3.6',
      zip_safe=True)
