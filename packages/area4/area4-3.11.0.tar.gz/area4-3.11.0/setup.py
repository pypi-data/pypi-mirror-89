"""Builds the package."""

import setuptools

# Package version:
VERSION = "3.11.0"

# Read the long description:
with open("README.md", mode="r") as FILE_HANDLER:
    LONG_DESCRIPTION = FILE_HANDLER.read()

keywords = ["area4", "dividers", "python", "utilities", "enhancements", "text"]

classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: Microsoft :: Windows :: Windows 8",
    "Operating System :: Microsoft :: Windows :: Windows 8.1",
    "Operating System :: Microsoft :: Windows :: Windows 7",
    "Operating System :: MacOS",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Other OS",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Topic :: System",
    "Topic :: Terminals",
    "Topic :: Text Processing",
    "Development Status :: 5 - Production/Stable",
    "Framework :: IDLE",
    "Natural Language :: English",
]

# GitHub URL:
homepage = "https://github.com/area4lib/area4"

# Other Project URLs:
urls = {
    "Bug Tracker": "https://github.com/area4lib/area4/issues",
    "Documentation": "https://area4.readthedocs.io/en/stable/",
    "Source Code": "https://github.com/area4lib/area4",
    "License": "https://github.com/area4lib/area4/blob/master/LICENSE",
}

setuptools.setup(
    name="area4",
    version=VERSION,
    author="Reece Dunham",
    author_email="me@rdil.rocks",
    maintainer="area4 Team",
    maintainer_email="me@rdil.rocks",
    description="Dividers in Python, the easy way!",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=homepage,
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=classifiers,
    project_urls=urls,
    keywords=keywords,
    include_package_data=True,
    zip_safe=False,
    python_requires=">3.3",
)
