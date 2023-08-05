import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lr_for_the_masses-SamV01", # Replace with your own username
    version="1.0.0",
    author="Samuel Vélez and Mandar Kathe ",
    author_email="samuelvelez@outlook.com",
    description="The purpose of this package is to provide simplified tools to apply several different linear regression models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samuel-velez/533_lab_4_KatheVelez",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)