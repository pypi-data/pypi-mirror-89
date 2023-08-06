import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="springbuk_de_bucket_download",
    version="0.0.1",
    author="Enrique Galindo",
    author_email="egalindo@springbuk.com",
    description="tool to download s3 buckets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EnriqueGalindo/springbuk_de_bucket_download",
    packages=setuptools.find_packages(),
    enty_points = {
        "console_scripts": [
            "dlt = download_tool_pkg.dt",
        ]
    }
)
