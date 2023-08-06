import setuptools

setuptools.setup(
    name="landscape-pdf", # Replace with your own username
    version="0.0.1",
    author="Niall Moran",
    author_email="niall@niallmoran.net",
    description="Utility to convert a pdf for viewing in landscape mode",
    long_description="Utility to convert a pdf for viewing in landscape mode",
    long_description_content_type="text/markdown",
    url="https://github.com/nmoran/landscape-pdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/landscape-pdf'],
    python_requires='>=3.6',
)