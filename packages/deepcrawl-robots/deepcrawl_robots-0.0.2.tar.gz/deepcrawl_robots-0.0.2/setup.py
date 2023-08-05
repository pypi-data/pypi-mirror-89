import setuptools

setuptools.setup(
    name="deepcrawl_robots",
    version="0.0.2",
    author="Andrei Mutu & Richard Barrett",
    author_email="support@deepcrawl.com",
    description="A package to bulk match urls to robots.txt files",
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(exclude=('tests',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
