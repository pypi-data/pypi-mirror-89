import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flagsup",
    version="0.0.1",
    author="Tri Tran",
    author_email="tri.tm@teko.vn",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)