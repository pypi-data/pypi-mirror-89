import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apricopt",
    version="0.0.1a1.dev3",
    author="Marco Esposito",
    author_email="esposito@di.uniroma1.it",
    description="A library for simulation-based parameter optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://mclab.di.uniroma1.it",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'attrs==20.3.0'
        'chaospy==4.2.1'
        'codetiming==1.2.0'
        'jsonschema==3.2.0'
        'numpy==1.19.4'
        'pandas==1.1.4'
        'petab==0.1.12'
        'pyparsing==2.4.7'
        'python-copasi==4.29.227'
        'python-dateutil==2.8.1'
        'PyYAML==5.3.1'
        'sympy==1.6.2'
    ],
    python_requires='>=3.6',
)