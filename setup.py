import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="social_media", 
    version="0.0.3.2",
    author="Atharva Naik",
    author_email="atharvanaik2018@gmail.com",
    description="Python package for scraping and automation of social media activity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atharva-naik/social_media",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=['tqdm', 'nltk', 'numpy', 'spacy', 'pandas', 'sklearn', 'pytube', 'requests', 'datetime', 'selenium', 'ansicolors', 'prettytable', 'webdriver_manager', 'python-dotenv', 'instabot'],
    python_requires='>=3.6',
)