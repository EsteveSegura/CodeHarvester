from setuptools import setup, find_packages

setup(
    name='CodeHarvester',
    version='1.0.0',
    author='Esteve Segura',
    author_email='estevesegura.gir@gmail.com',
    description='CodeHarvester efficiently aggregates code and text from files for streamlined AI analysis, simplifying data compilation and preparation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EsteveSegura/CodeHarvester',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Cython',
        'PyInstaller',
        'Flask',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'codeharvester=main:main',
        ],
    },
)
