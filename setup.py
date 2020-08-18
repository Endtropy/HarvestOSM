from setuptools import setup, find_packages

setup(
    name="harvestosm",
    packages=find_packages(),
    package_data={"": ["*.json"]},
    version="0.6",
    description="Tool for  generating Overpass queries and harvesting data from OpenStreetMap",
    long_description="See README.md",
    author="Michal Opletal",
    author_email="michal.opletal@gisat.cz",
    url="",
    license="",
    include_package_data=True,
    keywords=["openstreetmap", "overpass"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Utilities",
    ],
    install_requires=["requests>=2.22.0", "geojson>=2.5.0", "geopandas>=0.8", "shapely>=1.6.4"],
    extras_require={"test": ["unittest"]},
)