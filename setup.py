from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in medochemie/__init__.py
from medochemie import __version__ as version

setup(
	name="medochemie",
	version=version,
	description="Customization for ERPNext for Medochemie-specific use cases.",
	author="Medochemie",
	author_email="it@medochemie.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
