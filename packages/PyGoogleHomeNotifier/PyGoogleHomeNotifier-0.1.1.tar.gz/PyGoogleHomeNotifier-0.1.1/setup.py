import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requires = fh.read()

setuptools.setup(
    name = "PyGoogleHomeNotifier",
    version = "0.1.1",
    author = "k-sh",
    author_email = "tefutefu85@gmail.com",
    description = "google-home-notifier for python",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/k-sh/pygooglehomenotifier",
    packages = setuptools.find_packages(),
    install_requires = requires.splitlines(),
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6",
    keywords="pygooglehomenotifier PyGoogleHomeNotifier",
)

