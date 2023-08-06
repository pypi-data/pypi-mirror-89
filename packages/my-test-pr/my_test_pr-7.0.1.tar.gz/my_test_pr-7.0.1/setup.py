import setuptools


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements('requirements.txt')

setuptools.setup(
    name="my_test_pr",
    version="7.0.1",
    author="me",
    include_package_data=True,
    packages=['my_test_pr',
              'my_test_pr.code',
              ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=install_reqs
)
