from setuptools import setup, find_packages



classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name ="RJcalculator",
    version = "0.3.1",
    description = "A very basic calculator",
    long_description = "To access this package, download the .whl file given in the download links. Now, run the command 'pip install <file name> in powershell in the directory in which you have saved the file. Now your package is downloaded and you can import it. \n\nAlternatively, you can copy the above command and run it in powershell. You can mail me to ask any query. \n\nIf you already have this package installed and want to upgrade it to the latest version, run the command -\n\n 'pip install --upgrade ProjectName'.",
    author = 'Rachit Jain',
    author_email = 'jrachit012@gmail.com',
    License = 'MIT',
    classifiers = classifiers,
    keywords = 'calculator',
    packages = find_packages(),
    install_requires = []
)
