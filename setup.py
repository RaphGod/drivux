from setuptools import setup, find_packages

setup(
    name="drivux",
    version="0.1.0",
    description="GUI manager for OneDrive Linux client (abraunegg/onedrive)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rapha",
    url="https://github.com/RaphGod/drivux",
    license="GPL-3.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "drivux": ["resources/icons/*.svg"],
    },
    install_requires=[
        "PySide6>=6.5",
    ],
    entry_points={
        "console_scripts": [
            "drivux=drivux.main:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment",
        "Topic :: System :: Filesystems",
    ],
)
