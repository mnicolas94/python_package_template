import setuptools
from setuptools import find_packages
import subprocess
import sys


def get_last_version():
    bash_command = "git describe --tags --abbrev=0 --match v[0-9]*"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    outputstr = str(output)
    outputstr = outputstr[3:-3]  # "b'vXX.XX.XX\\n'" becomes "XX.XX.XX"
    outputstr = outputstr.replace('-', '.')
    exists_version = outputstr != ""
    if exists_version:
        major, minor, patch, *_ = outputstr.split('.')
        ver = f'{major}.{minor}.{patch}'
    else:
        ver = "0.1.0"
    return ver


def current_commit_has_tag():
    bash_command = "git describe --tags --exact-match HEAD"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    has_tag = output != b""
    return has_tag


def bump_patch(ver: str):
    major, minor, patch = ver.split('.')
    bumped = str(int(patch) + 1)
    return f'{major}.{minor}.{bumped}'


def push_new_version_as_tag(version):
    bash_command = f"git tag v{version}"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    bash_command = f"git push origin v{version}"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


if __name__ == '__main__':
    version = get_last_version()
    commit_has_tag = current_commit_has_tag()
    if not commit_has_tag:
        version = bump_patch(version)

    if sys.argv[1] == 'pushtag':
        if not commit_has_tag:
            push_new_version_as_tag(version)
    else:
        with open("README.md", "r") as fh:
            long_description = fh.read()

        setuptools.setup(
            name="***",
            version=version,
            author="Miguel Nicolás-Díaz",
            author_email="miguelcok27@gmail.com",
            description="***",
            long_description=long_description,
            long_description_content_type="text/markdown",
            url="https://github.com/mnicolas94/***",
            packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
            install_requires=[
                '***'
            ],
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
            ],
            python_requires='>=3.6',
        )
