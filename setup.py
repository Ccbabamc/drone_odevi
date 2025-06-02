from setuptools import setup, find_packages

setup(
    name="drone_delivery_system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "typing",
        "dataclasses",
    ],
    python_requires=">=3.7",
    author="Şevval",
    description="Drone teslimat sistemi optimizasyonu"
)