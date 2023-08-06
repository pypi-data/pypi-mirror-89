import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='RedPay',
    version='1.2.6',
    packages=['redpay'],
    url='https://bitbucket.org/redshepherdinc/python-api.git',
    author='Red Shepherd Inc.',
    author_email='support@redshepherd.com',
    description='Files for integrating with the RedPay Engine',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "pycryptodome>=3.9.9",
    ],
)
