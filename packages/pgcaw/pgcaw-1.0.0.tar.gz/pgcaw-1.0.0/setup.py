import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgcaw",
    version="1.0.0",
    author="Christian Godiksen",
    author_email="christian.godiksen55@gmail.com",
    description="PGCAW is a very simple API wrapper for the github contributions calendar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CGodiksen/pgcaw",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests', 'bs4'],
    keywords=['Github calendar', 'Github contributions', 'API', 'API Wrapper', 'Github'],
)