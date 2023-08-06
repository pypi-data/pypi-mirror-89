import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


setup(
    name="autoregressor",
    version="1.0.0",
    description="Automated entire process of building and training regression based models",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jaydulera/autoregressor",
    author="Jay Dulera",
    author_email="jaydulera01@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=["autoregressor"],
    include_package_data=True,
    install_requires=["sklearn", "pandas" , "numpy"],
    #entry_points={
        #"console_scripts": [
         #   "realpython=reader.__main__:main",
        #]
   # },
)