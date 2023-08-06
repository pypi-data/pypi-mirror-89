import setuptools

setuptools.setup(
    name="dolfin_warp",
    version="2020.12.23",
    author="Martin Genet",
    author_email="martin.genet@polytechnique.edu",
    description=open("README.md", "r").readlines()[1][:-1],
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/mgenet/dolfin_warp",
    packages=["dolfin_warp"],
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "vtk", "dolfin", "myPythonLibrary", "myVTKPythonLibrary", "dolfin_mech"],
)
