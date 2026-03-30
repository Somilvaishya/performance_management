from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="performance_management",
    version="0.0.1",
    description="Enterprise Task Intelligence System",
    author="Somil Vaishya",
    author_email="somilvaishya78@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
