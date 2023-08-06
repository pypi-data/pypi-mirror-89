from setuptools import setup
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

docs_reqs = [
    'mkdocs>=1.12'
    'mkdocstrings>=0.13.6'
    'mkdocs-material>=6.2.3'
]

extra_reqs = {
    'doc': docs_reqs
}

setup(
    name='scoutify',
    version='1.0.5',
    description='A simple Python wrapper library for Spotify WEB API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="@fijar-lazuardy",
    author_email="fijarlaz@gmail.com",
    url='https://github.com/samsan-tech/scoutify',
    install_requires=[
        'requests>=2.20.0',
        'six>=1.10.0',
    ],
    extras_require=extra_reqs,
    license='LICENSE.md',
    packages=['scoutify']
)
