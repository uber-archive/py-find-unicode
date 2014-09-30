from setuptools import setup, find_packages


setup(
    name="py-find-unicode",
    version="0.1.1",
    author="Evan Klitzke",
    author_email="evan@uber.com",
    url="https://github.com/uber/py-find-unicode",
    description="simple python ast consumer which searches for evil unicode",
    license='MIT (Expat)',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Security",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "py-find-unicode = py_find_unicode:main",
        ]
    },
    tests_require=["nose==1.3.0", "mock==1.0.1"],
    test_suite="nose.collector"
)
