import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="djist",
    version="0.1.0",
    author="liorelse",
    author_email="buggyfirmware@protonmail.com",
    description="Django-inspired static templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llelse/djist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.6',
)