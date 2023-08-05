from setuptools import setup


def read(fname):
    import os

    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="scipy-psdm",
    version="0.2.0",
    description=(
        "transform an ill-conditioned quadratic matrix to "
        "a positive semidefinite matrix"
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="http://github.com/ulf1/scipy-psdm",
    author="Ulf Hamster",
    author_email="554c46@gmail.com",
    license="MIT",
    packages=["scipy_psdm"],
    install_requires=["setuptools>=40.0.0", "numpy>=1.14.*", "scipy>=1.1.*"],
    python_requires=">=3.6",
    zip_safe=False,
)
