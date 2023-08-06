import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vis3dpy",
    version="0.0.2",
    description="Minimal 3D data visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LukasDrsman/vis3dpy",
    author="Lukáš Dršman",
    author_email="lukaskodr@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    install_requires=["PyOpenGL", "PyOpenGL_accelerate", "pygame"],
    python_requires='>=3.6'
)
