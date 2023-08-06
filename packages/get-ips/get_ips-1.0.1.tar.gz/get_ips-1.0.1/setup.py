from setuptools import setup, find_packages

VERSION = '1.0.1' 
DESCRIPTION = 'Get IPs'
LONG_DESCRIPTION = 'Get Public/Private IP'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="get_ips", 
        version=VERSION,
        author="Sven Wagner",
        author_email="svenw1612@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=["requests"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'ip', 'getip'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3.9",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)