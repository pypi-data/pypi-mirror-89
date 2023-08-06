from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tithiwa",
    version="0.1.30",
    description="tithiwa - Web WhatsApp bot: Automate Web WhatsApp with selenium in python.",
    py_modules=["chatroom", "constants", "flextithiwa", "group", "session", "messages", "tithiwa"],
    packages=find_packages(),
    package_dir={"tithiwa": "tithiwa"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    license="MIT License",
    entry_points={
        'console_scripts': [
            'tithiwa = tithiwa.__main__:main',
        ],
    },
    url="https://github.com/Tithibots/tithiwa",
    author="Navpreet Devpuri and Sulagna Mukherjee",
    author_email="NavpreetDevpuri@gmail.com",
    install_requires=[
        "selenium",
    ],
    extras_require={
        "dev": [
            "",
            "",
            "",
        ],
    },
)
