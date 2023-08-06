import setuptools

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `REQUIRES` value below.
REQUIRES = [
    'apscheduler',
    'docutils',
    'waitress',
    'watchdog',
    'wheel',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `DEV_REQUIRES` value in the Python
# dictionary below.
DEV_REQUIRES = [
]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyramid_task_scheduler',
    version='0.0.2',
    author='Patrick Magyar',
    author_email="magyarpatrick@gmail.com",
    description="task scheduler for pyramid framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: POSIX :: Linux",
     ],
    include_package_data=True,
    install_requires=REQUIRES,
    extras_require={
        'dev': DEV_REQUIRES,
    },
)
