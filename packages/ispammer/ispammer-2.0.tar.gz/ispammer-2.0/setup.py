from setuptools import setup, find_packages

with open('long_desc.txt', 'r') as desc:
    long_description = desc.read()

setup(
    name='ispammer',
    packages=find_packages(),
    include_package_data=True,
    version=2.0,
    description='A Free & Open Source Tool for Call/SMS Bombing on Indian Number ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='MrSp4rX',
    author_email='sparkykalund@gmail.com',
    url='https://github.com/MrSp4rX/iSpammer',
    download_url="https://github.com/MrSp4rX/iSpammer/archive/module.zip",
        keywords=['android', 'spam', 'sms', 'bomb', 'termux',
                  'sms-bomber', 'bomber', 'sms-bomb', 'bombing', 'call-bomb', 'ispammmer', 'mrsp4rx', 'indian-bombing', 'call-bombing'],
    install_requires=['requests'],
    license='GPL',
    entry_points={
            'console_scripts': [
                'ispammer = ispammer.ispammer:main',
            ],
    },
    python_requires='>=3.5'
)