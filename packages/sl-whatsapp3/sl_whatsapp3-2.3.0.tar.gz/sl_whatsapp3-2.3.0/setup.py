from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sl_whatsapp3",
    version="2.3.0",
    description="A Python pakege useing enemouse whatsapp fake message sending ",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shehan9909",
    author="shehan",
    author_email="shehan9909@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["BOMBER"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "sl_whatsapp3=BOMBER.whatsapp:main",
        ]
    },
)
