import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyVisualFields",
    version="1.0.2",
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
    install_requires = ["tzlocal >= 3.0",
            "tzlocal >= 3.0",
            "scikit-image >= 0.18.1",
            "pandas >= 1.2.4",
            "PyPDF2 >=  1.26.0",
            "PyMuPDF >= 1.19.1",
            "reportlab >=  3.6.2",
            "matplotlib >= 3.3.4" ],
    python_requires=">=3.6",
)

