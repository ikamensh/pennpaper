import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ilya_ezplot",
    version="0.0.3",
    author="Ilya Kamenshchikov",
    author_email="ikamenshchikov@gmail.com",
    description="Set of utilities for ploting results of non-deterministic experiments, "
                "e.g. machine learning, optimization, genetic algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ikamensh/ddpg",
    packages=["ilya_ezplot",
              "ilya_ezplot.metric",
              "ilya_ezplot.plot",
              "ilya_ezplot.processing",],
    package_dir={'ilya_ezplot': 'ilya_ezplot'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)