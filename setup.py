import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="violent_webdriver",
    version="1.0.3",
    author="Yuyi Shao",
    author_email="523314409@qq.com",
    description="violent webdriver based on selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amazingTest/violent_webdriver",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)