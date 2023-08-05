import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezSMS", # Replace with your own username
    version="0.3.0",
    author="Tilak Patel",
    author_email="tilakpat@outlook.com",
    description="A small package that allows you to send easy SMS messages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TilakPatel/pypi-easy-sms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
