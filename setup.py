import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyVisualFields",
    version="1.0.0",
    author="Mohammad Eslami",
    author_email="Mohammad_eslami@meei.harvard.edu",
    description="A python toolkit for visual field analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohaEs/PyVisualField",
    project_urls={
        "Bug Tracker": "https://github.com/mohaEs/PyVisualField/issues",
        "Demo Normalization": "https://github.com/mohaEs/PyVisualField/blob/main/demo_2_Deviation_Analysis.ipynb",
        "Demo Plotting": "https://github.com/mohaEs/PyVisualField/blob/main/demo_3_Plotting.ipynb",
        "Demo Analysis": "https://github.com/mohaEs/PyVisualField/blob/main/demo_4_Analysis.ipynb",
        "Demo Data": "https://github.com/mohaEs/PyVisualField/blob/main/demo_1_Data.ipynb",    
        "Harvard Ophthalmology AI LAB": "https://ophai.hms.harvard.edu/" 
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

