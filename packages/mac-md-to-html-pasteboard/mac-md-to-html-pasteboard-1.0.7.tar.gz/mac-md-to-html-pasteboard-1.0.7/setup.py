import setuptools

version = None

with open('VERSION', 'r') as f:
    version = f.read()

setuptools.setup(
    name="mac-md-to-html-pasteboard",
    version=version,
    author="Sasha Friedenberg",
    author_email="carley.f253fa96@icantbelieveitsnotgmail.com",
    description="""reads markdown from stdin and uses pandoc and pyobjc to copy
    styled html as public.html to the macOS pasteboard""",
    url="https://github.com/friedenberg/mac-md-to-html-pasteboard",
    packages=['mac_md_to_html_pasteboard'],
    package_data={
        'mac-md-to-html-pasteboard': ['mac_md_to_html_pasteboard/styles/'],
        },
    include_package_data=True,
    install_requires=['pyobjc-core', 'pyobjc-framework-Cocoa', 'pypandoc'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: MacOS X :: Cocoa",
    ],
    python_requires='>=3.7.6',
    entry_points = {
        'console_scripts': ['md-to-html-pasteboard = mac_md_to_html_pasteboard.__main__:main'],
    }
)
