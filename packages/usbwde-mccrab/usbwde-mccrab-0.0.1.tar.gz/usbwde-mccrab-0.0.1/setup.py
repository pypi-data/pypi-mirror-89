import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='usbwde-mccrab',
    version='0.0.1',
    author='Gabe Krabbe',
    author_email='krabbe@google.com',
    description='A client class for the USB-WDE1 receiver by ELV.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mccrab/usbwde',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
    install_requires=[
        'pyserial',
    ],
    python_requires='>=3.6',
)
