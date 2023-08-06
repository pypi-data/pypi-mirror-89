import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezsend", # Replace with your own username
    version="0.0.4",
    author="Eshan Nalajala",
    author_email="eshan.nalajala@gmail.com",
    description="Ezsend, the easiest way to send mail and texts in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BouncyBird/ezsend",
    packages=setuptools.find_packages(),
    install_requires=[
        'sys',
        're',
        'smtplib',
        'time', 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
