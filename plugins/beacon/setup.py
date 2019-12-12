from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name="alerta-beacon",
    version=version,
    description='Alerta plugin for Beacon',
    url='https://github.com/ernadhalilovic/alerta-contrib',
    license='MIT',
    author='Ernad Halilovic',
    author_email='ehalilovic@wayfair.com',
    packages=find_packages(),
    py_modules=['alerta_beacon'],
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.plugins': [
            'beacon = alerta_beacon:ServiceIntegration'
        ]
    }
)
