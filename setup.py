from setuptools import setup, find_packages


setup(
    name="pavlok",
    version="0.1.0",
    license="MIT",
    author="Maneesh Sethi",
    author_email="maneesh@pavlok.com",
    packages=find_packages("pavlok"),
    package_dir={"": "pavlok"},
    url="https://github.com/Pavlok/pavlok-python-client",
    keywords="pavlok",
    install_requires=[
        "Authlib==0.15.4",
        "fastapi==0.68.1",
        "pydantic==1.8.2",
        "python-dotenv==0.19.0",
        "starlette==0.14.2",
        "uvicorn==0.15.0",
    ],
)
