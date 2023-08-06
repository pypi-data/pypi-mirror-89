import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chessAnalyzer",  # Replace with your own username
    version="0.0.1",
    author="Aryan Anand",
    author_email="aryananand.chess@gmail.com",
    description="Analyses games and positions. Possible to have a Game Report similar to the one from chess.com, "
                "including graphs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CoderAryanAnand/pythonChessAnalyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
