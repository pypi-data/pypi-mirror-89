from setuptools import setup
setup(
    name = "python-indodax", 
    packages = ["indodax"], 
    version = "0.0.1", 
    license="MIT", 
    description = "Python wrapper for indodax.com API", 
    author = "Faisal Malik Widya Prasetya", 
    author_email = "faisalmalikwidyaprasetya@gmail.com", 
    url = "https://github.com/MasiCal354/python-indodax", 
    download_url = "https://github.com/MasiCal354/python-indodax/archive/v_01.tar.gz", 
    keywords = ["indodax", "vipbtc", "api"], 
    install_requires=["requests","pandas"],
    classifiers=[
        "Development Status :: 3 - Alpha", 
        "Intended Audience :: Developers", 
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)