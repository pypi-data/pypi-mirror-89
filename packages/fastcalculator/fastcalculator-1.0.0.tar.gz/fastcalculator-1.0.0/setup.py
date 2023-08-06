from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='fastcalculator',
    version='1.0.0',
    description='A very basic calculator',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Praveen',
    author_email='praveen885127@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='calcultors',
    packages=find_packages(),
    install_requires=['']
)