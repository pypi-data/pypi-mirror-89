from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    required = fh.read().splitlines()

setup(
    name='francium',
    version='0.0.3.dev1',
    packages=['francium', 'francium.core', 'francium.algorithms', 'francium.algorithms.hill_climbing',
              'francium.algorithms.genetic_algorithm', 'francium.algorithms.simulated_annealing'],
    url='https://github.com/satyajitghana/ProjektFrancium',
    license='',
    author='Satyajit Ghana',
    author_email='satyajitghana7@gmail.com',
    description='A simple library for testing out AI Algorithms',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
    include_package_data=True,
)
