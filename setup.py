from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

from bizflow_integrations import __version__ as version

setup(
	name='bizflow_integrations',
	version=version,
	description='Modular Integrations for Frappe Apps (WhatsApp, IndiaMart, Google Ads)',
	author='Nexgen ERP Technologies',
	author_email='info@nexgenerp.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
