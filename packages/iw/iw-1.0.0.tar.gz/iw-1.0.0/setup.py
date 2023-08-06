import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="iw",
    version="1.0.0",
    description="Insightful information from insightworkshop.io",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/shrawanx/iw",
    author="Insight Workshop",
    author_email="shrawan@insightworkshop.io",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["iw"],
    include_package_data=True,
)
