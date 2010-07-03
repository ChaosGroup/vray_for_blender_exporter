'''
  V-Ray/Blender 2.5
'''

import sys

WITH_BF_INTERNATIONAL = 'true'
WITH_BF_JPEG = 'true'
WITH_BF_PNG = 'true'
WITH_BF_OPENEXR = 'true'
WITH_BF_FFMPEG = 'true'
WITH_BF_OPENAL = 'true'
WITH_BF_SDL = 'true'
WITH_BF_BULLET = 'true'
WITH_BF_ZLIB = 'true'
WITH_BF_FTGL = 'true'

WITH_BF_QUICKTIME = 'false'
WITH_BF_FMOD = 'false'
WITH_BF_ICONV = 'false'
WITH_BF_STATICOPENGL = 'false'
WITH_BF_VERSE = 'false'
WITH_BF_GAMEENGINE = 'false'
WITH_BF_PLAYER = 'false'

WITH_BF_COLLADA = 'false'
WITH_BF_RAYOPTIMIZATION= 'true'

WITH_BUILDINFO = 'true'

BF_OPENAL_LIB = 'openal alut'
BF_TWEAK_MODE = 'false'
BF_PYTHON_VERSION = '3.1'

BF_DEBUG = 'false'

if(sys.platform == "win32"):
	BF_NUMJOBS = 4
	
	BF_SPLIT_SRC= 'true'

	BF_BUILDDIR = 'C:\\b'
	BF_INSTALLDIR = 'C:\\release\\vrayblender-2.5.02'
	BF_DOCDIR='C:\\release\\vrayblender-2.5.02\\doc'

else:
	# Optimize for Intel Core
	#CCFLAGS = ['-pipe','-fPIC','-march=nocona','-msse3','-mmmx','-mfpmath=sse','-funsigned-char','-fno-strict-aliasing','-ftracer','-fomit-frame-pointer','-finline-functions','-ffast-math']
	#CXXFLAGS = CCFLAGS
	#REL_CFLAGS = ['-O3','-fomit-frame-pointer','-funroll-loops']
	#REL_CCFLAGS = REL_CFLAGS

	CCFLAGS = ['-pipe','-fPIC','-funsigned-char','-fno-strict-aliasing']
	CPPFLAGS = ['-DXP_UNIX']
	CXXFLAGS = ['-pipe','-fPIC','-funsigned-char','-fno-strict-aliasing']
	REL_CFLAGS = ['-O2']
	REL_CCFLAGS = ['-O2']

	C_WARN = ['-Wno-char-subscripts', '-Wdeclaration-after-statement']
	CC_WARN = ['-Wall']

	# Just because some gcc 4.4 bug that cause segfault
	#CC= 'gcc-4.3'
	#CXX= 'g++-4.3'

	BF_NUMJOBS = 4
	BF_BUILDDIR = '/tmp/build-vrayblender-25'
	BF_INSTALLDIR = '/opt/vrayblender-2.5.02'
	BF_DOCDIR='/opt/vrayblender-2.5/doc'
	
