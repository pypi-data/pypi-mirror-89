"""Install five-in-row and dependencies."""

import sys
from setuptools import setup


def get_package_version() -> str:
    """Read package version from env variable or VERSION file"""
    optional_version_parameter = sys.argv[-1]

    if optional_version_parameter.startswith('--version'):
        version = optional_version_parameter.split("=")[1]
    else:
        with open('VERSION') as version_file:
            version = version_file.read().strip()

    return version


def get_readme() -> str:
    """Read README as a text."""
    with open('README.md', encoding='utf-8') as f:
        return f.read()


def main() -> None:
    setup(
        name='five-in-row',
        version=get_package_version(),
        python_requires='>=3.7',
        description='Framework for playing piskvorky.jobs.cz',
        long_description=get_readme(),
        long_description_content_type='text/markdown',
        url='https://github.com/JakubTesarek/five',
        author='Jakub Tesárek',
        author_email='jakub@tesarek.me',
        license='GPL-3',
        include_package_data=True,
        packages=['five_in_row'],
        install_requires=[
            'requests',
            'numpy'
        ],
        extras_require={
            'dev': [
                'setuptools',
                'wheel',
                'pytest',
                'pytest-cov',
                'pytest-mock',
                'pytest-benchmark',
                'requests-mock',
                'mypy',
                'flake8',
                'flake8-colors',
                'flake8-eradicate',
                'flake8-print',
                'flake8-todo',
                'twine'
            ],
        }
    )


if __name__ == '__main__':
    main()
