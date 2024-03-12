from setuptools import setup, find_packages

setup(
    name="scanman",
    version="1.0.1",
    description="Using LLMs to interact with man pages",
    url="https://github.com/nikhilkmr300/scanman",
    author="Nikhil Kumar",
    author_email="nikhilkmr300@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "faiss-cpu",
        "langchain",
        "langchain-openai",
        "langchainhub",
        "openai",
        "termcolor"
    ],
)
