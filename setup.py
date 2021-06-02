import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastpreprocess",
    version="0.1.7",
    entry_points = {
        'console_scripts': [
            'fastpreprocess = fastpreprocess.fastwork:run_from_local',
            'fp = fastpreprocess.fastwork:run_from_local'
        ],
    },
    author="Lal Krishna Arjun",
    author_email="lk.arjun@hotmail.com",
    description="A new way to preprocess data for ML.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/lkarjun/fastpreprocess",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "uvicorn==0.13.4",
        "pydantic==1.8.2",
        "numpy==1.20.3",
        "python-multipart",
        "fastapi==0.65.1",
        "pandas==1.2.4",
        "tqdm==4.60.0",
        "jinja2==2.11.3",
        "pyngrok==5.0.5",
        "nest-asyncio==1.5.1",
        "aiofiles==0.7.0",
        "httptools==0.2.0",
    ],
    package_data={"fastpreprocess": ["template/*", "static/*"]},
    include_package_data = True
)

