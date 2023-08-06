from setuptools import setup, find_packages

setup(
    name='BLUvo',
    version='0.7',
    license='MIT',
    description='API Wrapper for the Bluelink/Uvo service',
    author='William Comartin',
    author_email='williamcomartin@gmail.com',
    url='https://github.com/wcomartin/bluvo',
    download_url='https://github.com/wcomartin/bluvo/archive/v_0.7.tar.gz',
    keywords=['Kia', 'Uvo', 'Api', 'bluelink'],
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
