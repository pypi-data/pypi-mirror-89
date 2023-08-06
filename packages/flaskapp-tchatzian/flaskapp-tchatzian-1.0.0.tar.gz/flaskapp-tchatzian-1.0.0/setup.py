
from setuptools import find_packages
from setuptools import setup

setup(
        name='flaskapp-tchatzian',
        version='1.0.0',
        description='contains some sample hello world code using Flask',
        author='tchatzian',
        author_email='harischatzi1988@gmail.com',
        url='https://github.com/tchatzian/offlinemap',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
                    'flask',
        ],
        entry_points={
		'console_scripts':[
			'flaskapp=src.app:main',
		],
	},
)
