from setuptools import setup, find_packages

# version
version_globals = {}
with open("version.py") as vf:
    exec(vf.read(), version_globals)
version = version_globals["__version__"]

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    author="Marcos Jesus Vivar",
    author_email="marcos.vivar@protonmail.com",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8'
    ],
    description="Python SDK for space agencies RESTful APIs",
    download_url=f"https://github.com/ultraeia/PyAstrum/archive/{version}.tar.gz",
    install_requires=['json_log_formatter',
                      'future',
                      'requests'
                    ],
    include_package_data=True,
    license="MIT License",
    long_description = long_description,
    long_description_content_type='text/markdown',
    name="PyAstrum",
    packages = find_packages(),
    project_urls={
        #'Funding': 'https://donate.pypi.org/PyAstrum',
        'Source': 'https://github.com/ultraeia/PyAstrum',
        #'Tracker': 'https://github.com/ultraeia/PyAstrum/issues',
    },
    python_requires='>=3.8',
    url="https://github.com/ultraeia/PyAstrum",
    version=version,
)