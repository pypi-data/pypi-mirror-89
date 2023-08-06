import setuptools

with open('./README.md') as readme_file:
  readme = readme_file.read()

setuptools.setup(
    name='notipy_osx',
    version='0.0.9',
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    license='MIT',
    url='https://notipy.now.sh/',
    project_urls={
        "Bug Tracker": "https://github.com/ninest/aquaui/issues",
        "Documentation": "https://github.com/ninest/aquaui",
        "Source Code": "https://github.com/ninest/aquaui",
    },
    long_description_content_type="text/markdown",
    description='Deprecated, use aquaui instead',
    long_description=readme,
)

'''
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*

'''