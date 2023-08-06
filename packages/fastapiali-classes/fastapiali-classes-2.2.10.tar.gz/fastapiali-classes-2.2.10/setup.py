from setuptools import setup

setup(
    name='fastapiali-classes',
    version='2.2.10',
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/giaca95/Fastapiali-classes',
    download_url="https://github.com/giaca95/Fastapiali-classes.git",
    license='MIT',
    author='giaca95',
    author_email='giacomo_callegaro.95@libero.it',
    description='Classi per poter creare oggeti da usare con fastapi',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'SQLAlchemy>=1.3.22',
        'Pydantic>=1.7.3',
        'fastapi-modules>=2.2.7',
        'FastAPI-SQLAlchemy>=0.2.1'
    ]
)
