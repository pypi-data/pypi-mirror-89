import setuptools
from pathlib import Path


setuptools.setup(
    name="pdfconverter1309",
    version=1.0,
    long_description=Path("README.md").read_text(),
    include_package_data=True
)
