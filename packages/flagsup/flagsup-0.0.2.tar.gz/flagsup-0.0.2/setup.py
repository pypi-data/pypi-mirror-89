import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flagsup",
    version="0.0.2",
    author="Tri Tran",
    author_email="tri.tm@teko.vn",
    description="A Feature Flags management SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
)
