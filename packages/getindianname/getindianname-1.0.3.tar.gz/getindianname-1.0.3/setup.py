import setuptools
import requests
#with open("README.md", "r") as file:
 #   readme = file.read()

readme = requests.get("https://raw.githubusercontent.com/devesh7272/getindianname/main/README.md").text

setuptools.setup(
	name="getindianname",
	version="1.0.3",
	author="Devesh Singh",
	author_email="connect.world12345@gmail.com",
	description="Get 30K+ random Indian names",
	long_description=readme,
	long_description_content_type="text/markdown",
	url="https://github.com/devesh7272/getindianname",
	license="MIT",
	classifiers=["License :: OSI Approved :: MIT License"],
	packages=["getindianname"],
	include_package_data=True,
	python_requires='>=2.0',

)
