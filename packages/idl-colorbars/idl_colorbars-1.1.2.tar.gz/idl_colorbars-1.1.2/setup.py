import setuptools

setuptools.setup(
    name='idl_colorbars',
    version='1.1.2',
    description='Load IDL colormaps into matplotlib.',
    url='https://github.com/planetarymike/idl-colorbars-python',
    author=('Mike Chaffin'),
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.10',
        'matplotlib>=3.0.3'],
)
