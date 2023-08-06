import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="event_analytics", 
    version="0.1.0",
    author="Babel Pte. Ltd",
    author_email="contact@babel.sg",
    description="An Event Analytics package to help organizers analyze, segment & understand Audience & their behavior. Built with love by Babel!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/babel-data/event_analytics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
