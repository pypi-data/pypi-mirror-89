import setuptools

setuptools.setup(
    name="simple-docker-deploy-script",
    version="0.0.1",
    author="Anielkis Herrera",
    author_email="aherrera@zato.io",
    description="A script to deploy a Docker container",
    long_description="A simple script used to deploy a test image to Docker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
