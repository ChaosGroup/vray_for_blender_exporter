#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import inspect
import os
import sys
import traceback
import time
import datetime

import bpy


MsgTypeToColor = {
    'ERROR'  : 'red',
    'INFO'   : 'blue',
    'NORMAL' : 'none',
}

def Color(text, color=None):
    if not color or sys.platform == 'win32':
        return text
    if color == 'green':
        return "\033[0;32m%s\033[0m" % text
    elif color == 'red':
        return "\033[0;31m%s\033[0m" % text
    elif color == 'blue':
        return "\033[0;34m%s\033[0m" % text
    elif color == 'yellow':
        return "\033[0;33m%s\033[0m" % text
    elif color == 'magenta':
        return "\033[0;35m%s\033[0m" % text
    else:
        return text


def IsDebugMode():
    if hasattr(bpy.context, 'scene'):
        if bpy.context.scene.vray.Exporter.debug:
            return True
    return False


# Log message
#
def PrintInfo(message, msgType='NORMAL'):
    sys.stdout.write("%s: %s\n" % (
        Color("V-Ray For Blender", 'green'),
        Color(message, MsgTypeToColor[msgType]),
    ))
    sys.stdout.flush()


def PrintError(message):
    Debug(message, msgType='ERROR')


def Debug(message, msgType='NORMAL'):
    if not IsDebugMode() and msgType in {'NORMAL'}:
        return
    PrintInfo(message, msgType)


# Prints fancy dict
#
def PrintDict(title, params, spacing=2):
    Debug("%s:" % title)
    for key in sorted(params.keys()):
        if type(params[key]) == dict:
            spacing *= 2
            PrintDict(key, params[key], spacing)
            spacing /= 2
        elif type(params[key]) in (list,tuple):
            Debug("%s%s" % (''.join([' ']*int(spacing)), Color(key, 'yellow')))
            for item in params[key]:
                Debug(''.join([' ']*int(spacing)*2) + str(item))
        else:
            Debug("%s%s: %s" % (''.join([' ']*int(spacing)), Color(key, 'yellow'), params[key]))


# https://gist.github.com/techtonik/2151727
#
def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]
    name = []
    module = inspect.getmodule(parentframe)
    if module:
        name.append(module.__name__)
    if 'self' in parentframe.f_locals:
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':
        name.append(codename)
    del parentframe
    return ".".join(name)


def ExceptionInfo(e):
    if not IsDebugMode():
        return

    exc_type, exc_value, exc_traceback = sys.exc_info()

    print("Exception => '%s': %s" % (type(e).__name__, e))
    print("Traceback =>")

    traceback.print_tb(exc_traceback)


def TimeIt(method):
    def timed(*args, **kw):
        if IsDebugMode():
            sys.stdout.write(Color("V-Ray For Blender", 'green'))
            sys.stdout.write(": %s()...\n" % method.__name__)
            sys.stdout.flush()
        ts = time.time()
        result = method(*args, **kw)
        te = time.time() - ts
        td = datetime.timedelta(seconds=te)
        if IsDebugMode():
            sys.stdout.write(Color("V-Ray For Blender", 'green'))
            sys.stdout.write(": %s() done [%s].\n" % (method.__name__, str(td)))
            sys.stdout.flush()
        return result
    return timed
