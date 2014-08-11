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

import json
import os
import pathlib
import sys

from . import SysUtils


PLUGINS_DESC = {}


def GetPluginsDescDir():
    return os.path.join(SysUtils.GetExporterPath(), "plugins_desc")


def LoadPluginDesc():
    descDirpath = pathlib.Path(GetPluginsDescDir())

    for filePath in descDirpath.iterdir():
        if not filePath.name.endswith('.json'):
            continue

        pluginDesc = json.loads(filePath.open().read())

        pluginID     = pluginDesc.get('ID')
        pluginParams = pluginDesc.get('Parameters')
        pluginName   = pluginDesc.get('Name')
        plguinWidget = pluginDesc.get('Widget', {})

        PLUGINS_DESC[pluginID] = {
            'ID'         : pluginID,
            'Name'       : pluginName,
            'Parameters' : pluginParams,
            'Widget'     : plguinWidget,
        }


def GetPluginParams(pluginID):
    if pluginID in PLUGINS_DESC:
        return PLUGINS_DESC[pluginID]['Parameters']
    return []


def GetPluginWidget(pluginID):
    if pluginID in PLUGINS_DESC:
        # TODO: Finish plugins this way and refactor this
        return json.dumps(PLUGINS_DESC[pluginID]['Widget'])
    return {}


def PluginName(pluginName):
    if pluginName[0].isdigit():
        pluginName = "PL%s" % pluginName
    return pluginName
