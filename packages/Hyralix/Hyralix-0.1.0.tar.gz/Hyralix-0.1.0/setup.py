from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: Other/Proprietary License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Hyralix',
    version='0.1.0',
    description='Hyralix is a basic text formatter for Python.',
    long_description='Hyralix is a basic text formatter for Python.',
    url='',
    author='Oliwier Sporny',
    author_email='info.paradoxentertainment@gmail.com',
    license='Proprietary',
    classifiers=classifiers,
    keywords='text, formatting, python, color, colour, proprietary, hyralix',
    packages=find_packages(),
    install_requires=['']
)
