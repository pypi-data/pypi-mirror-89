import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    include_package_data=True,
    name="python-gender", # Replace with your own username
    version="0.0.3",
    author="Aimé Risson",
    author_email="aime.risson.1@gmail.com",
    description="A python gender classification package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aime-risson/python-gender-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['joblib','pandas']

)