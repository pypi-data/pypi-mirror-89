import setuptools

setuptools.setup(
    name='valoStatus',
    version='0.0.1',
    author='D3CRYPT360',
    description='A python library to check for riot games server status for VALORANT without an API key',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/D3CRYPT360/valStatus',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>= 3.6',
    keywords='valorant''gaming''gamers', 
    include_package_data=True,
    install_requires=['requests']
)