from distutils.core import setup

setup (
	name='dropcopy',
	version='1.0',
	description='A simple tool to copy a given GnuCash file to a local dropbox directory whenever it is saved.',
	author='Francisco Carlos Luz Barros Junior',
	author_email='juniorbl@gmail.com',
	url='http://github.com/juniorbl/dropcopy',
	scripts=["dropcopy-run.py"],
	packages=['dropcopy'],
	license='MIT License',
	data_files=[
		('share/applications', ['dropcopy.desktop']),
		('usr/share/icons/hicolor/16x16/apps', ['icons/16x16/dropcopy-logo.png']),
		('usr/share/icons/hicolor/22x22/apps', ['icons/22x22/dropcopy-logo.png']),
		('usr/share/icons/hicolor/48x48/apps', ['icons/48x48/dropcopy-logo.png'])]
)
