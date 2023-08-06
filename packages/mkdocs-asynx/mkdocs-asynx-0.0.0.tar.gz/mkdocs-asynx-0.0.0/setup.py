import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mkdocs-asynx",
    version="0.0.0",
    author="Alper Yazar",
    description="A pluging makes asynx.dev Team to build https://asynx.dev",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asynx-dev/mkdocs-asynx-plugin",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Topic :: Documentation",
        'Topic :: Text Processing',
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-asynx = mkasynx.entry:Entry',
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        'mkdocs >= 1.1'
    ]
)
