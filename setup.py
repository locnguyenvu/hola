import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="locnguyenvu-hola",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "psycopg2-binary",
        "Flask",
        "Flask-JWT-Extended",
        "Flask-SQLAlchemy",
    ]
)