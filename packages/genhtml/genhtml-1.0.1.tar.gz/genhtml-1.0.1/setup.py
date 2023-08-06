import setuptools

long_description = '''
Generate HTML. Usage:
	import genhtml
	html=genhtml.HTML()
	p=html.open('p')
	p.attrs['style']='color:red;'
	p.write('Hello!')
	p.close()
	html.commit(p)
	html.open_in_browser()
	print(html.output())
'''

setuptools.setup(
    name="genhtml", # Replace with your own username
    version="1.0.1",
    author='Vadim Simakin',
    author_email="sima.vad@gmail.com",
    description="Html5 generator",
    long_description=long_description,
    long_description_content_type="text/plain",
    packages=['genhtml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)