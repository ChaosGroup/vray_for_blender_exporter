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

    for filePath in descDirpath.glob("*/*.json"):
        file = filePath.open()
        pluginDesc = json.loads(file.read())
        file.close()

        pluginID      = pluginDesc.get('ID')
        pluginParams  = pluginDesc.get('Parameters')
        pluginName    = pluginDesc.get('Name')
        pluginType    = pluginDesc.get('Type')
        pluginSubType = pluginDesc.get('Subtype', None)
        pluginIDDesc  = pluginDesc.get('Description', "")
        pluginWidget  = pluginDesc.get('Widget', {})

        PLUGINS_DESC[pluginID] = {
            # To match plugin interface
            # XXX: Refactor
            'DESC'         : pluginIDDesc,
            'ID'           : pluginID,
            'NAME'         : pluginName,
            'SUBTYPE'      : pluginSubType,
            'TYPE'         : pluginType,
            'Name'         : pluginName,
            'Parameters'   : pluginParams,
            'PluginParams' : pluginParams,
            'PluginWidget' : pluginWidget,
            'Widget'       : pluginWidget,
        }


def loadPluginOnModule(plugin, pluginID):
    if pluginID in PLUGINS_DESC:
        pluginDesc = PLUGINS_DESC[pluginID]

        for key in pluginDesc:
            plugin[key] = pluginDesc[key]


def PluginName(pluginName):
    if pluginName[0].isdigit():
        pluginName = "PL%s" % pluginName
    return pluginName
