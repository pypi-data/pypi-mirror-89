import setuptools

with open("README.md","r",encoding="utf-8") as fh:
              long_description=fh.read()
          
setuptools.setup(
    name="metaClean",
    version="0.4.2",
    author="veggieburger",
    author_email="veggies4dayz@protonmail.com",
    description="Auto Clean Pictures MetaData",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/veggieburger/metaclean.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security",
        ],
    python_requires='>=3.8',
    scripts=['metaClean'],
    data_files = [('metaCleanConfig',['metaCleanConfig/config.yml','metaCleanConfig/metaClean.service.org'])],
)
    


