from setuptools import setup, find_packages

setup(
    name="locnguyenvu-hola",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp",
        "alembic",
        "beautifulsoup4",
        "Flask",
        "Flask-JWT-Extended",
        "Flask-SQLAlchemy",
        "flask-cors",
        "python-dateutil",
        "python-dotenv",
        "python-telegram-bot",
        "psycopg2-binary",
        "requests",
        "rich",
    ],
    extras_require={
        "production": [
            "uWSGI",
        ]
    }
)
