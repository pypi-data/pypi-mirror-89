from setuptools import setup, find_packages
setup(
       # the name must match the folder name 'verysimplemodule'
        name="Package-p", 
        version='0.0.1',
        author="Prakash Choudhary",
        author_email="<choudharyprakash066@gmail.com>",
        description="Test",
        long_description="Test Package",
        packages=find_packages(),
        install_requires=[], 
        keywords=['python', 'first package'],
        
)