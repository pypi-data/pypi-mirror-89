import setuptools

setuptools.setup(
    name="fimodule",
    version="0.0.2",
    license='MIT',
    author="FSanchir",
    author_email="fsanchir@fsip.ml",
    description="Fi bot's developing Module",
    long_description=open('README.md', 'rt', encoding='UTF8').read(),
    long_description_content_type="text/markdown",
    url="https://dl.fsip.ml/",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp', 'discord', 'discord.py'
    ],
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)