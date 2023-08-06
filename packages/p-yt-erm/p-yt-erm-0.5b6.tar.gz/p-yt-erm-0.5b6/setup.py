import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='p-yt-erm',
    version='0.5b6',
    author='Anne & Lynice',
    maintainer='Alex Technically',
    maintainer_email='alexa@nicolor.tech',
    description='Easy to use youtube music streamer command line tool written in python3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pYTerm'],
    entry_points={
        'console_scripts': [
            'pYTerm=pYTerm.pYTerm:commandline',
        ],
        
    },
    url='https://gitlab.com/mocchapi/pyterminal/',
    install_requires=[
        'python-vlc',
        'pafy',
        'beautifulsoup4',
        'youtube-dl',
        'pypresence',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.8'
)
