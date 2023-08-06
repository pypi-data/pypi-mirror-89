import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
    name="henipipe",
    version="1.65",
    author="Scott Furlan",
    author_email="scottfurlan@gmail.com",
    description="A python wrapper for fast and parallel processing of sequencing data using CutnRun or CutnTag",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scfurl/henipipe.git",
    packages=setuptools.find_packages(),
    package_data={'henipipe': ['henipipe/data/genomes.json']},
    install_requires=['six >= 1'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.5',
    entry_points={'console_scripts': [
        'henipipe = henipipe.__main__:run_henipipe',
        'samTobed = henipipe.samTobed:run_sam2bed',
        'pyWriter = henipipe.pyWriter:run_pyWriter',
        'auc = henipipe.auc:run_auc',
    ]},
    )


"""
#TEST PyPI
## run this to make package: python3 setup.py sdist bdist_wheel
## run this to upload to test pypi: twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#TEST INSTALL
# pip install --index-url https://test.pypi.org/henipipe/ henipipe


#FOR REAL
cd ~/OneDrive\ -\ Fred\ Hutchinson\ Cancer\ Research\ Center/computation/develop/henipipe/
rm dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
scfurl


##Install pipx
## python3 -m pip install --user pipx
## python3 -m pipx ensurepath

**At SCRI do the following**

module load python
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install --include-deps --pip-args '--trusted-host pypi.org --trusted-host files.pythonhosted.org' henipipe
pipx install --spec git+https://github.com/scfurl/henipipe --include-deps henipipe --pip-args '--trusted-host pypi.org --trusted-host files.pythonhosted.org'
pipx install --spec git+https://github.com/scfurl/henipipe@cleaner --include-deps henipipe --pip-args '--trusted-host pypi.org --trusted-host files.pythonhosted.org'


**At the FHCRC do the following...**

module load Python/3.6.7-foss-2016b-fh1
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install --include-deps henipipe
pipx install git+https://github.com/scfurl/henipipe --include-deps
pipx uninstall henipipe


pipx uninstall henipipe
pipx install git+https://github.com/scfurl/henipipe --include-deps

"""