from setuptools import setup, find_packages
classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'Programming Language :: Python :: 3'
]

setup(
	name='cmdperfect',
	version='0.3',
	description='Hy, this is cool librari for making cmd programs more beautifull and easy',
	long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	url='',
	auther='Davide Harutyunyan',
	auther_email='davidework2419@gmail.com',
	license='MIT',
	classifiers=classifiers,
	keywords='cmd display perfect cmdperfect perfectcmd cool',
	packages=find_packages(),
	install_requires=['']
	)