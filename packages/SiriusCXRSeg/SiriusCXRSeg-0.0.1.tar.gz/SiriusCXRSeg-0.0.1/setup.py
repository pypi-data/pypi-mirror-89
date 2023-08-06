import setuptools
from setuptools import find_packages, setup

setup(
	name='SiriusCXRSeg',
	version="0.0.1",
    	author="Sirius_nauka16",
    	 author_email="dkhasanov76@gmail.com",
   	 description="Проект по сегментации легких.",
         packages=find_packages(),
	 package_data = {
		'SiriusSeg': [
		    'trained_models/Model_all_heart_v2',
		]
    		},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
    			],
	python_requires='>=3.6.9',
)

