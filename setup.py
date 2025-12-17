"""
Setup configuration for Marketing Content Engine
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="marketing-content-engine",
    version="1.0.0",
    author="Marketing Content Engine Team",
    description="AI-powered engine for automated video content creation and distribution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nishchith-m1015/Marketing-Content-Engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Marketing Professionals",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "Topic :: Office/Business :: Marketing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "openai>=1.0.0",
        "anthropic>=0.8.0",
        "pillow>=10.0.0",
        "moviepy>=1.0.3",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "sqlalchemy>=2.0.0",
        "redis>=5.0.0",
        "python-dateutil>=2.8.2",
        "validators>=0.22.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "marketing-engine=engine:main",
        ],
    },
)
