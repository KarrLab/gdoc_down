from setuptools import setup, find_packages
import os

# get long description
if os.path.isfile('README.rst'):
    with open('README.rst', 'r') as file:
        long_description = file.read()
else:
    long_description = ''

# get version
with open('gdoc_down/VERSION', 'r') as file:
    version = file.read().strip()

# parse requirements.txt
install_requires = [line.rstrip() for line in open('requirements.txt')]
tests_require = [line.rstrip() for line in open('tests/requirements.txt')]

setup(
    name="gdoc_down",
    version=version,
    description="Download Google documents to files",
    long_description=long_description,
    url="https://github.com/KarrLab/gdoc_down",
    download_url='https://github.com/KarrLab/gdoc_down',
    author="Jonathan Karr",
    author_email="jonrkarr@gmail.com",
    license="MIT",
    keywords='Google documents drive download latex tex html pdf docx',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={
        'gdoc_down': [
            'VERSION',
            'client.json',
        ],
    },
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications :: File Sharing',
        'Topic :: Office/Business :: Office Suites',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'gdoc_down = gdoc_down.__main__:main',
        ],
    },
)
