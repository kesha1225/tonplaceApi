from setuptools import setup, find_packages
import tonplace


setup(
    name="tonplaceapi",
    version=tonplace.__version__,
    url="https://github.com/kesha1225/tonplaceApi",
    author="kesha1225",
    packages=find_packages(),
    description="ton.place wrapper",
    install_requires=["aiohttp"],
    long_description=open("README.md", encoding="utf-8").read(),
)