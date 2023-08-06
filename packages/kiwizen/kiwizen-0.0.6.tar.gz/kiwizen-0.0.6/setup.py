from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kiwizen',
    version='0.0.6',
    description='Many pieces of useful python code',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Zen Shawn',
    author_email='xiaozisheng2008@qq.com',
    maintainer='Zen Shawn',
    maintainer_email='xiaozisheng2008@qq.com',
    license='BSD License',
    # packages=find_packages(),
    packages=['kiwizen.adb', 'kiwizen.plt', 'kiwizen.alg', 'kiwizen.common', 'kiwizen.tools', 'kiwizen.wechat', 'kiwizen.'],
    platforms=["all"],
    url='https://gitee.com/zen_shawn/Kiwi.git',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'scipy', 'matplotlib', 'coloredlogs==14.0'],
    python_requires=">=3.5"
)
