from setuptools import find_packages, setup

setup(
    name = 'shreyagajbhiye',
    version = '0.0.1',
    author = 'shreya gajbhiye',
    author_email = 'gajbhiyeshreya23@gmail.com',
    install_requires = ["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages = find_packages()
)