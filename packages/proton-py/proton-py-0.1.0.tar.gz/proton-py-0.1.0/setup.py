import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proton-py",
    version="0.1.0",
    author="rodneymandap",
    author_email="rodneyjan.mandap@gmail.com",
    description="Python package to connect to IWG Proton API",
    long_description=long_description,
    url="https://github.com/rodneymandap/iwg-proton",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=['requests'],
)