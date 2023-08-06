import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nospamplus",
    version="1.0",
    author="Leo",
    url="http://nospamplus.tk",
    license='License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    author_email="dev@nospamplus.tk",
    description="A Python Wrapper For Nospamplusapi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["requests >= 2.22.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)