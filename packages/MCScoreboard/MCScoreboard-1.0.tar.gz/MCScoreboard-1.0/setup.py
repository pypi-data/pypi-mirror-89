import setuptools


setuptools.setup(
    name="MCScoreboard",
    version="1.0",
    author="Frank Ruan",
    author_email="rsboss01@outlook.com",
    description="A simple python3 software helps you to create Minecraft Scoreboard",
    url="https://github.com/orange2008/minecraft-scoreboard-manual",
    packages=setuptools.find_packages(),
    install_requires=['matplotlib','numpy','pygal'],
    entry_points={
        'console_scripts': [
            'mcsb=mcsb:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
