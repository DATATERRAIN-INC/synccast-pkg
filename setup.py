# setup.py
from setuptools import setup, find_packages

# Pull version from _version.py
version = {}
with open("synccast/_version.py", encoding='utf-8') as f:
    exec(f.read(), version)

setup(
    name="syncast",
    version=version["VERSION"],  # <- Use your manual version string
    description="Real-time communication and UI sync framework for Django using MQTT",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Smaraka Ranjan Parida B",
    author_email="smarka@dataterrain.com",
    url="https://github.com/smarakaranjan/synccast",
    packages=find_packages(include=["synccast", "synccast.*"]),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "requests",
        "pytest",
        "pytest-django"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
