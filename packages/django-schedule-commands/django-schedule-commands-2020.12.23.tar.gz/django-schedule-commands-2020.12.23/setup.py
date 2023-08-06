import setuptools

setuptools.setup(
    name='django-schedule-commands',
    version='2020.12.23',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
