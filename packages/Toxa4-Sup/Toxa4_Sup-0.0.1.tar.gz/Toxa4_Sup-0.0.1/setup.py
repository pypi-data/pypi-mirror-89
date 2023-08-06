import setuptools



with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
requirements = ["requests<=2.21.0", "pyowm<=3.1.1"]
setuptools.setup(
	name="Toxa4_Sup",
	version="0.0.1",
	author="Dima Zyryanov",
	author_email="dima.terig02@gmail.com",
	description="This is my 1st project ",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/dimaterig0404",
	packages=setuptools.find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.5',
)