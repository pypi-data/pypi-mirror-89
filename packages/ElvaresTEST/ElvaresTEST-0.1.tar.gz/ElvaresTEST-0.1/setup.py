import setuptools


# def parse_requirements(filename):
#     """ load requirements from a pip requirements file """
#     lineiter = (line.strip() for line in open(filename))
#     return [line for line in lineiter if line and not line.startswith("#")]


# install_reqs = parse_requirements('requirements.txt')

setuptools.setup(
    name="ElvaresTEST",
    version="0.1",
    author="EL",
    url = 'https://github.com/Elvares/PrintTestFunc',
    author_email="elvares251997@gmail.com",
    description="Library for ElvaresTEST",
    packages=['ElvaresTEST'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ]
)
