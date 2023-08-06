from setuptools import setup, find_packages
import os

long_description  = "sample-python-package"
long_description += "This is a basic Python module and you can simply add this by using this command."
long_description += "pip install kcalculator or pip3 install kcalculator"

long_description += "Note:-"
long_description += "It basicly perform on addition, subtraction, multiply or divide operations."
long_description += "for Now it perform only basic operation."
long_description += "Ex: - a +b 2+3 = 5"
long_description += "How to use this package"
long_description += "from calc import calc"
long_description += "print(calc.Number.add_numberes(4,5))"
long_description += "This package works for only add_numbers, subtact_numbers, multy_numbers, divide_numbers"

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# with open(BASE_DIR+"/README.md", "r") as fh:
#     long_description = fh.read()
classification = [
	'Development status :: 5 - Production/stable',
	'Intended Audience :: Education',
	'Operating System :: Linux :: ubuntu',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: PYthon :: 3'
]

setup(
	name='kcalculator',
	version='0.0.10',
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
	install_requires=[''],
	py_modules=['calc.calc'],
)

