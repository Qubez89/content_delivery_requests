from setuptools import setup, find_packages

setup(
    name="content_delivery_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.0",
        "pymongo>=4.0",
    ],
    entry_points={
        "console_scripts": [
            "delivery-app=streamlit_app:main",
        ],
    },
)