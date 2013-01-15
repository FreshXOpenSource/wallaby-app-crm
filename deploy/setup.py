from setuptools import setup, find_packages
import wallaby.FX as FX
import sys

try:
    import py2exe
except: pass

import wallaby.apps.inspector

packages = find_packages('.')
includes = ['twisted', 'pkgutil', 'sip', 'json', 'PyQt4.QtCore', 'PyQt4.QtGui']
#wallabyPackages, _ = FX.wallabyPackages([])
wallabyPackages = ["wallaby", "zope.interface"]

VERSION = '0.1.32'
LICENSE = 'GNU Lesser General Public License (LGPL)'

APP = ['app.py']


PY2EXE_OPTIONS = {
        'includes': includes,
        'packages': wallabyPackages,
        'dll_excludes': ['MSVCP90.dll'],
        'excludes' :  ['_tkagg','_ps','_fltkagg','Tkinter','Tkconstants',
                      '_agg','_cairo','_gtk','gtkcairo','pydoc','sqlite3',
                      'bsddb','curses','tcl',
                      '_wxagg','_gtagg','_cocoaagg','_wx'],
        }

PY2APP_OPTIONS = {
        'strip': False, 
        'argv_emulation': True, 
        # 'semi_standalone': True, 
        'iconfile': 'wallaby.icns',
        # 'site_packages': True, 
        # 'optimize': 2,
        # 'compressed': False,
        'includes': includes,
        'packages': wallabyPackages,
    'excludes' :  ['_tkagg','_ps','_fltkagg','Tkinter','Tkconstants',
                      '_agg','_cairo','_gtk','gtkcairo','pydoc','sqlite3',
                      'bsddb','curses','tcl',
                      '_wxagg','_gtagg','_cocoaagg','_wx'],
    'plist'    : {  'CFBundleDisplayName': 'crm',
                    'CFBundleGetInfoString' : 'wallaby, FreshX',
                    'CFBundleIdentifier':'com.freshx.wallaby',
                    'CFBundleShortVersionString':VERSION,
                    'CFBundleVersion': 'crm ' + VERSION,
                    'CFBundleIconFile': 'wallaby.icns',
                    'LSMinimumSystemVersion':'10.7',
                    'LSMultipleInstancesProhibited':'false',
                    'NSHumanReadableCopyright':LICENSE
                }}

if len(sys.argv) > 1 and sys.argv[1] not in("copy"):
    setup(name='wallaby-app-crm',
      version=VERSION,
      url='http://freshx.de/wallaby/apps/crm',
      author='FreshX GbR',
      author_email='wallaby@freshx.de',

      windows=[{'script':'app.py', 'icon_resources':[(0, 'wallaby.ico')]}],
      app=APP,
      license=LICENSE,
 
      packages=packages,
      install_requires=['wallaby-app-inspector', 'wallaby-plugin-pdfgenerator'],
      include_package_data = True,

      options={'py2app': PY2APP_OPTIONS, 'py2exe': PY2EXE_OPTIONS},
      # setup_requires=['macholib', 'modulegraph', 'py2app', 'py2exe'],
  )

if len(sys.argv) > 1 and sys.argv[1] in("py2app", "copy"):
    print '*** Removing Qt debug libs ***'
    import os
    for root, dirs, files in os.walk('./dist'):
        for file in files:
            # if 'debug' in file:
            #     print 'Deleting', file
            #     os.remove(os.path.join(root,file))
            if 'test_' in file:
                print 'Deleting', file
                os.remove(os.path.join(root,file))
            elif '_tests' in file:
                print 'Deleting', file
                os.remove(os.path.join(root,file))
            # elif '.pyc' in file:
            #     print 'Deleting', file
            #     os.remove(os.path.join(root,file))
    
    os.chdir('./dist')
    # os.system(r'macdeployqt crm.app -dmg -verbose=0')
    os.system(r'macdeployqt wallaby-app-crm.app -verbose=0')
    os.chdir('..')
    
    os.system(r'hdiutil create crm-mac-' + VERSION + r'.dmg -volname "wallaby@fx" -fs HFS+ -srcfolder "dist"')
