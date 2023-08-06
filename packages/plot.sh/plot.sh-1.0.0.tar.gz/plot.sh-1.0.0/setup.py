from setuptools import find_packages, setup

setup(
    name='plot.sh',
    version='1.0.0',
    description='plot.sh client tool',
    url='https://plot.sh',
    author='Lars Volker',
    author_email='help@plot.sh',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
