import setuptools

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="raisin",
    version="0.0.13",
    author="Robin RICHARD (robinechuca)",
    author_email="raisin@ecomail.fr",
    description="Simple parallel, distributed and cluster computing",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://framagit.org/robinechuca/raisin",
    packages=setuptools.find_packages(),
    install_requires=["pycryptodomex", "cloudpickle"], # ces paquets serons installes d'office
    extras_require={
        "calculation": ["sympy", "giacpy", "numpy"],
        "tools": ["psutil>=5.1", "regex", "cloudpickle"],
        "graphical": ["tkinter", "matplotlib"],
        "security": ["pycryptodomex"]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords=["parallel", "distributed", "cluster computing"],
    python_requires=">=3.6",
)
