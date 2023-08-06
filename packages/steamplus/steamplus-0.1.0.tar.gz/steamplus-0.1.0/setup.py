from setuptools import find_packages, setup

setup(
    name="steamplus",
    packages=find_packages(include=["steamplus"]),
    version="0.1.0",
    license="GPL-3.0-only",
    description="A library for extracting data from steam via steam storefront api and steamspy api",
    author="Team Ster",
    author_email="martijn.business@hotmail.com",
    url="https://github.com/MartijnCBV/steamplus/wiki",
    download_url="https://github.com/MartijnCBV/steamplus/archive/0.1.0.tar.gz",
    keywords=["steam", "statistics", "valve"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest===6.2.1"],
    test_suite="tests"
)
