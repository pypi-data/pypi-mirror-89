from setuptools import setup

setup(
    name="pytorch-quantum",
    version="0.1-dev-3",
    description="A PyTorch based library for Quantum Machine Learning",
    url="http://github.com/pytorch-quantum",
    author_email="contact@anuragsaharoy.me",
    include_package_data=True,
    packages=[
        "pytorch_quantum",
        ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy==1.19.0", 
        "scipy==1.5.4",
        "torch==1.7.1", 
        "pytorch-lightning==1.1.1",
    ],
    python_requires=">=3.6",    
)