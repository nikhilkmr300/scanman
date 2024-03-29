from setuptools import setup, find_packages

setup(
    name="scanman",
    description="Using LLMs to interact with man pages",
    url="https://github.com/nikhilkmr300/scanman",
    version="1.0.3",
    author="Nikhil Kumar",
    author_email="nikhilkmr300@gmail.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "faiss-cpu",
        "langchain",
        "langchain-openai",
        "langchainhub",
        "openai",
        "termcolor",
    ],
    entry_points={
        "console_scripts": [
            "scanman = scanman.__main__:main",
        ]
    },
)
