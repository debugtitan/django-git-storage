from setuptools import setup


description = (
    'Django Github Storage Package '
)

setup(
    name='django-git-storages',
    version='0.0.6',
    author='Uche David',
    author_email='debugtitan.hub@outlook.com',
    description=description,
    long_description="Django package that facilitates integration with Github as it's storage provider",
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/debugtitan/django-git-storage',
    keywords=['django git storage','django github storage'],
    packages=['git_storage'],
    include_package_data=True,
    classifiers = [
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ]
)