from setuptools import setup, find_packages

setup(
    name="blog-automatcao",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'requests'
    ]
)
