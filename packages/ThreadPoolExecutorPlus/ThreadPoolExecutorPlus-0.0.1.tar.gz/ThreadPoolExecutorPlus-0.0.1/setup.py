from setuptools import setup, find_packages

setup(
    name="ThreadPoolExecutorPlus",
    version='0.0.1',
    author="WEN",
    description="A fully replaceable executor that makes it possible to reuse idle threads and shrink thread list when there's no heavy load.",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/GoodManWEN/ThreadPoolExecutorPlus",
    packages = find_packages(),
    install_requires = [],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.4',
    keywords=["concurrent.futures" , "threading" , "multi-threads" ,"ThreadPoolExecutor"]
)