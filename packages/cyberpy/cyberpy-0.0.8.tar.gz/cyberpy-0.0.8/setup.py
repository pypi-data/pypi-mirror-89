from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cyberpy',
    version='0.0.8',
    packages=['cyberpy'],
    url='https://github.com/SaveTheAles/cyberpy',
    license='MIT',
    author='alpuchilo',
    author_email='ales.puchilo@gmail.com',
    description='Tools for Cyber wallet management, offline transaction signing and broadcasting',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'ecdsa',
        'bech32',
        'hdwallets',
        'mnemonic',
        'typing-extensions',
        'requests'
      ]
)
