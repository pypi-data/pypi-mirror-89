import setuptools  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pipe_stat",
    version="0.0.3",
    author="Leon Morten Richter",
    author_email="leon.morten@gmail.com",
    description="Get the status of your GitLab pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/M0r13n/pipe-stat",
    license="MIT",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'pipe-stat = pipe_stat.main:main',
        ],
    },
    package_data={
        "pipe_stat": ["py.typed"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Typing :: Typed",
    ],
    keywords=["Gitlab", "Pipeline", "Status", "Monitor"],
    python_requires='>=3.6',
    install_requires=[
        "python-gitlab",
        "tabulate",
        "python-dateutil"
    ]
)
