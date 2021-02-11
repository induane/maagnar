from setuptools import setup, find_packages


setup(
    name="maagnar",
    version="1.0.1",
    url="https://github.com/induane/maagnar",
    author="Brant Watson",
    author_email="oldspiceap@gmail.com",
    description="Library and command line entry point for generating anagrams",
    long_description="Library and command line entry point for generating anagrams",
    license="MIT License",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["log_color"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["maagnar = maagnar.entry_point:main"]},
)
