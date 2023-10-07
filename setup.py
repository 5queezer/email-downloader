from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

setup(
    name='email_download',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    license='MIT',
    description='Downloads email from IMAP server',
    author='Christian Pojoni',
    author_email='christian.pojoni@gmail.com'
)
