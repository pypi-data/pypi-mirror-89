from setuptools import setup
from Cython.Build import cythonize
import numpy as np
from distutils.extension import Extension
import logging
import sys


def parse_requirements(filename):
	"""Load requirements from a pip requirements file."""
	with open(filename) as f:
		lineiter = (line.strip() for line in f)
		return [line for line in lineiter if line and not line.startswith("#")]

# Set up the logging environment
logging.basicConfig()
log = logging.getLogger()

# Check Cython installation
try:
	from Cython.Build import cythonize
except:
	log.critical(
		'Cython.Build.cythonize not found. '
		'Cython is required to build from a repo.')
	sys.exit(1)

# Extension options
include_dirs = []
try:
	import numpy
	include_dirs.append(numpy.get_include())
except ImportError:
	log.critical('Numpy and its headers are required to run setup(). Exiting')
	sys.exit(1)


opts = dict(
	include_dirs=include_dirs,
)
ext_modules = cythonize([
	Extension(
		'sslap.auction_', ['sslap/auction_.pyx'], **opts),
	Extension(
		'sslap.feasibility_', ['sslap/feasibility_.pyx'], ** opts)
]
)

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name='sslap',
	version='0.1.3.6',
	description='Super Sparse Linear Assignment Problems Solver',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author_email='ollieboyne@gmail.com',
	url='http://github.com/OllieBoyne/sslap',
	author='Ollie Boyne',
	ext_modules = ext_modules,
	install_requires=parse_requirements('requirements.txt'),
	license="MIT",
	keywords='super sparse linear assignment problem solve lap auction algorithm',
)
