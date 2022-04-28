import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyVisualFields",
    version="0.0.1",
    author="Mohammad Eslami",
    author_email="Mohammad_eslami@meei.harvard.edu",
    description="A python toolkit for visual field analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohaEs/PyVisualField",
    project_urls={
        "Bug Tracker": "https://github.com/mohaEs/PyVisualField/issues",
        "Demo Data": "https://github.com/mohaEs/PyVisualField/blob/main/demo_1_Data.ipynb",
        "Demo Analysis": "https://github.com/mohaEs/PyVisualField/blob/main/demo_2_Analysis.ipynb",
        "Demo Plotting": "https://github.com/mohaEs/PyVisualField/blob/main/demo_3_Plotting.ipynb",
        "Demo Normalization": "https://github.com/mohaEs/PyVisualField/blob/main/demo_4_Normalization_Deviation_Analysis.ipynb",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "PyVisualFields"},
    packages=setuptools.find_packages(where="PyVisualFields"),
    python_requires=">=3.6",
)

