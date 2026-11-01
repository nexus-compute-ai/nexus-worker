from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="nexus-worker",
    version="0.1.1",
    description="Provider daemon for NexusCompute: Monetize your GPU by serving AI inference.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexus-compute-ai/nexus-worker",
    project_urls={
        "Homepage": "https://nexus-compute.pages.dev",
        "Repository": "https://github.com/nexus-compute-ai/nexus-worker",
        "Documentation": "https://github.com/nexus-compute-ai/nexus-worker#readme",
    },
    packages=find_packages(),
    install_requires=[
        "httpx>=0.27.0",
        "websockets>=12.0",
        "click>=8.1.7",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "nexus-worker = nexus_worker.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
)
