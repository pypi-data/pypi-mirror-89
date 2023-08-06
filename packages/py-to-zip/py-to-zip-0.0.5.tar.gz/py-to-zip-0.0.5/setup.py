import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='py-to-zip',
    version='0.0.5',
    license='MIT',
    description='py-to-zip is a Python library that creates a zip file and a command file from your python code',
    author='matan h',
    author_email='matan.honig2@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/matan-h/czip',
    packages=['py_to_zip'],
    scripts=['py_to_zip\\CZip.bat'],
    package_data={'py_to_zip': ["license.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
