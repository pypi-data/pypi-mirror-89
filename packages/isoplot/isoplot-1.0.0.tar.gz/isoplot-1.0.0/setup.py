import setuptools
import re

with open("README.rst", "r") as fh:
    long_description = fh.read()
	
# Version is maintained in the __init__.py file
with open("isoplot/__init__.py") as f:
    try:
        VERSION = re.findall(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setuptools.setup(
	name="isoplot",
	version=VERSION,
	url="https://github.com/LoloPopoPy/Isoplot2",
    author="Loïc Le Grégam",
    author_email="loic.le-gregam@insa-toulouse.fr",
	license='GPLv3',
	description='Generate figures from Isocor output',
    classifiers=["Development Status :: 4 - Beta",
                "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                "Natural Language :: French",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Topic :: Scientific/Engineering :: Bio-Informatics"],
    long_description=long_description,
	long_description_content_type="text/x-rst",
	packages = setuptools.find_packages(),
    install_requires = [
        "numpy>=1.19.1",
        "pandas>=1.1.1",
        "matplotlib>=3.3.1",
        "seaborn>=0.10.1",
        "natsort>=7.0.1",
        "bokeh==2.0.2",
		"ipywidgets>=7.5.1",
        "colorcet>=2.0.2",
        "openpyxl>=3.0.5",
        "xlrd>=1.2.0"
    ], 
	entry_points={
        'console_scripts': [
            'isoplot = isoplot.isoplotcli:initialize_cli',
        ]},
)