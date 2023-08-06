import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speak_heAR",
    version="0.0.1",
    author="Rohan Lal Kshetry",
    author_email="rlkshetry95@gmail.com",
    description="speak and take command functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rohan-LK/py_speak_heaR.git",
    packages=setuptools.find_packages(),
    py_modules = ['speak_heAR'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
