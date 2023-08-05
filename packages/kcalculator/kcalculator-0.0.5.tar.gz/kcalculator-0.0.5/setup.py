from setuptools import setup, find_packages

# read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()
print(long_description)
classification = [
	'Development status :: 5 - Production/stable',
	'Intended Audience :: Education',
	'Operating System :: Linux :: ubuntu',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: PYthon :: 3'
]

setup(
	name='kcalculator',
	version='0.0.5',
	description='A baisc calulcator',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/softprodigyofficial/sample-python-package.git',
	author='kuldeep khatana',
	author_email='kuldeep.si.softprodigy@gmail.com',
	License='MIT',
	classifiers=[
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	],
	keywords='calulcator',
	package=find_packages(),
	install_requires=['']


)
