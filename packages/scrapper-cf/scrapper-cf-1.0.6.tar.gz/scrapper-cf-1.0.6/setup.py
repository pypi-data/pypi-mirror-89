import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="scrapper-cf",
    version="1.0.6",
    description="This library is aimed at speeding up making of scrappers. The 'utils.py' file contains useful functions which allows users to raise alerts, get random user agents and hit URLs at random. This also reduces chances of getting blocked by the server ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.codefree.io/",
    author="Codefree.io",
    author_email="wilson@codefree.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["scrapper"],
    include_package_data=True,
    install_requires=[''],
    # data_files=[('Data', ['user_agents.csv'])],
    # package_data={'Scrapper': ['Data/*.csv']},
    python_requires='>3.5'
   
)