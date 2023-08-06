from setuptools import setup
from setuptools import find_packages

requirements = ['pillow',
                'string',
                'os',
                'textwrap',
                'string']

setup(
    name='textimage',
    version='1.0.0',
    description='puts text on image',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='HYKANTUS',
    author_email='hykantus@gmail.com',
    License='MIT',
    classifiers=[],
    keywords='Pillow, PIL, Image Manipulation, text, text on image',
    packages=find_packages(),
    install_requires=requirements
)
