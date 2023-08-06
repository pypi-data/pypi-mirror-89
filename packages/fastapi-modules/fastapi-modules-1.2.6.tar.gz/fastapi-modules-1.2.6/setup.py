from setuptools import setup, find_packages


setup(
    name='fastapi-modules',
    version='1.2.6',
    packages=find_packages(),
    author="Gaicomo Callegaro",
    author_email="giacomo_callegaro.95@libero.it",
    description="Pacchetto per i modelli di fastapi sqlalchemy",
    install_requires=[
        'SQLAlchemy>=1.3.22',
        'Pydantic>=1.7.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    url='https://github.com/giaca95/models',
    download_url='https://github.com/giaca95/models.git'
)
