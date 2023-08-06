from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name = 'django-magic-tables',
    version = '0.3.3.0',
    description = 'A Django app to turn easily QuerySets into tables',
    long_description_content_type= 'text/markdown',
    long_description = README,
    url = 'https://gitlab.com/gabrymattioli/django-magic-tables',
    author = 'Gabriele Mattioli',
    author_email = 'gabrymattioli@gmail.com',
    license = 'MIT', 
    packages=find_packages(),
    keywords= ['Table', 'Magictable'],
    download_url='https://pypi.org/project/django-magic-tables/',
)

if __name__ == "__main__":
    setup(**setup_args, include_package_data=True)

