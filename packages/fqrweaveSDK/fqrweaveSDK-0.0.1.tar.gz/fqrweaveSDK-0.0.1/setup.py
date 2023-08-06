from distutils.core import setup






setup(
    name="fqrweaveSDK",
    packages=["fqrweaveSDK"],
    version="0.0.1",
    description="SDK to interact with fQR Weave platform",
    url="https://github.com/fQR-Weave/arweave-sdk",
    author="wojak-frog",
    author_email="fqrweave@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",

    ],

    include_package_data=True,
    install_requires=[
        "arweave-python-client"
    ]
)