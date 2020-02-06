from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name                = 'tootorch',
    version             = '0.1',
    long_description    = long_description,
    long_description_content_type = 'text/markdown',
    description         = 'Implemetation XAI in Computer Vision (Pytorch)',
    author              = 'Jaehuck Heo',
    author_email        = 'wogur379@gmail.com',
    url                 = 'https://github.com/TooTouch/tootorch',
    download_url        = 'https://github.com/TooTouch/tootorch/archive/v0.1.tar.gz',
    install_requires    =  ["torch","torchvision","h5py","tqdm","pillow","opencv-python"],
    packages            = find_packages(exclude = []),
    keywords            = ['tootorch','XAI'],
    python_requires     = '>=3.6',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)