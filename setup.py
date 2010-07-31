from distutils.core import setup

setup (
	name='dropcopy',
	version='1.0',
	description='A simple tool to copy a given GnuCash file to a local dropbox directory whenever it is saved.',
	author='Francisco Carlos Luz Barros Junior',
	author_email='juniorbl@gmail.com',
	url='http://github.com/juniorbl/dropcopy',
	scripts=["dropcopy-run.py"],
	license='MIT License',
	packages=['dropcopy'],
	package_data={'dropcopy':['icons/*.png']},
)
