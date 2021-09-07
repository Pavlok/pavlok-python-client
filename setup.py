from setuptools import setup, find_packages


setup(
    name='pavlok',
    version='0.1.0',
    license='MIT',
    author="Maneesh Sethi",
    author_email='maneesh@pavlok.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Pavlok/pavlok-python-client',
    keywords='pavlok',
    install_requires=[
        'Authlib==0.15.4',
        'fastapi',
        'pydantic==1.8.2',
        'python-dotenv==0.19.0',
        'starlette',
        'starsessions==1.1.0',
        'urllib3==1.26.6',
        'uvicorn==0.15.0'
      ],

)