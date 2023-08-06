import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-radius-eap-mschapv2-authbackend", 
    version="1.0",
    author="mneitsabes",
    author_email="mneitsabes@nulloz.be",
    description="A Django RADIUS EAP-MSCHAPv2 Authentication Backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
	keywords = ['radius', 'EAP', 'MSCHAPv2', 'django', 'backend', 'auth'],
    url="https://github.com/mneitsabes/RADIUS-EAP-MSCHAPv2-Python-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[       
          'radius-eap-mschapv2-client',
      ],
    python_requires='>=3.6',
)