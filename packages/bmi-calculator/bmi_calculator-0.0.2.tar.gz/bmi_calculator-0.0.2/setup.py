import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="bmi_calculator",
    version="0.0.2",
    author="Eromosele Iriogbe",
    author_email="eiriogbe@gmail.com",
    description="Calculates BMI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EronzG/BMI_library",
    packages=setuptools.find_packages(),
    install_requires=[''],  # if you have libraries that your module depen
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
