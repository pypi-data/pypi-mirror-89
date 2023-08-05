from setuptools import setup, find_packages

base_packages = ["numpy>=1.15.4", "scipy>=1.2.0"]

dev_packages = [
    "flake8>=3.6.0",
    "pytest==4.0.2",
    "jupyter==1.0.0",
    "jupyterlab==0.35.4",
]


setup(
    name="calmcode",
    version="0.0.2",
    packages=find_packages(exclude=["notebooks"]),
    install_requires=base_packages,
    extras_require={"dev": dev_packages},
)
