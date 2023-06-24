from setuptools import setup, find_packages

setup(
    name="locnguyenvu-hola",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp >= 3.8.1",
        "alembic >= 1.8.0",
        "beautifulsoup4 >= 4.11.1",
        "Flask >= 2.1.2",
        "Flask-JWT-Extended >= 4.4.1",
        "Flask-SQLAlchemy >= 2.5.1",
        "flask-cors >= 3.0.10",
        "python-dateutil >= 2.8.2",
        "python-dotenv >= 1.0.0",
        "python-telegram-bot == 13.12",
        "psycopg2-binary >= 2.9.3;sys_platform=='linux' or sys_platform=='darwin'",
        "requests >= 2.28.0",
        "rich",
    ],
    extras_require={
        "production": [
            "uWSGI",
        ]
    }
)
