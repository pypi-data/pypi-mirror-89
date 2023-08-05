import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="placavehiculos-pkg-aquintero535", # Replace with your own username
    version="1.0.0",
    author="Adrian Quintero",
    author_email="adrianquintero61@gmail.com",
    description="Paquete de aplicacion que verifica la placa de un vehiculo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/progllladrian/placa-vehiculos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)