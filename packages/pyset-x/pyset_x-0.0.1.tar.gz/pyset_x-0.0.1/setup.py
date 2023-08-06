import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyset_x', # Replace with your own username
    version='0.0.1',
    author='Christian Zinck',
    author_email='christian.zinck@gmail.com',
    description='Like `set -x` in bash',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/czinck/pyset_x',
    packages=setuptools.find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
    install_requires=['astroid']
)
