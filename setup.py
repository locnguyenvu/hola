from setuptools import setup, find_packages

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
        "flask-cors",
        "uWSGI",
        "python-telegram-bot",
        "python-dotenv",
        "beautifulsoup4",
        "requests"
    ],
    extras_require={
        "dev": [
            "rich",
            "python-dateutil",
            "alembic"
        ]
    }
)
