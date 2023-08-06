from setuptools import setup

setup(
    name='phoneme_guesser',
    version='0.1.0',
    packages=['phoneme_guesser'],
    url='https://github.com/OpenJarbas/phoneme_guesser',
    include_package_data=True,
    install_requires=["unidecode"],
    license='Apache2',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    description='phonemes from text'
)
