import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyteleprint", # Replace with your own username
    version="1.0.3",
    author="Rojit George",
    author_email="rojitrgeorge@gmail.com",
    description="A package for remote program alerts,prints and notification through Telegram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krrgeorges/pyteleprint",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)