from setuptools import setup

setup(
    name='vainu-dateutil',
    version="2020.12.0",
    packages=['vainu.dateutil'],
    url='https://vainu.io/',
    license='Proprietary',
    author='Vainu Finland Oy',
    author_email='kimmo@vainu.io',
    description='Vainu specific date-related utilities.',
    install_requires=[
        "python-dateutil",
        # Runtime requirements go here
    ]
)
