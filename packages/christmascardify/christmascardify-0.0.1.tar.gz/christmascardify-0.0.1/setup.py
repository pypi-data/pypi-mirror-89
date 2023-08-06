from setuptools import setup
import os

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(name='christmascardify',
      version='0.0.1',
      description='Automate your christmas card creation!',
      long_description=open("README.md").read(),
      long_description_content_type='text/markdown',
      author='Rahul Prabhu',
      author_email='rahul@grokwithrahul.com',
      url='https://github.com/grokwithrahul/christmas-card-creator',
      packages=['christmascardify'],
      install_requires=['Pillow']
     )