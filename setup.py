# from pkg_resources import parse_requirements
from setuptools import setup

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

reqs = parse_requirements('requirements.txt')
print(reqs)

setup(
    name='pybry',
    version='0.1',
    author='dev@recoilvelocity.com',
    author_email='dev@recoilvelocity.com',
    url="https://github.com/selner/pybry",
    install_requires=reqs,
    packages=['pybry', 'pybry.config', 'pybry.database', 'pybry.datatypes', 'pybry.decorators', 'pybry.pluginmanager',
              'pybry.utils'],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "pybry"},
    # packages=setuptools.find_packages(where="pybry"),
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # setup_requires=parse_requirements('requirements/build.txt'),
    # tests_require=parse_requirements('requirements/tests.txt'),
    # install_requires=[
    #     "setuptools>=45.0",
    # ],
    # extras_require={
    #     'all': parse_requirements('requirements.txt'),
    #     # 'tests': parse_requirements('requirements/tests.txt'),
    #     # 'build': parse_requirements('requirements/build.txt'),
    #     # 'optional': parse_requirements('requirements/optional.txt'),
    # },
)
