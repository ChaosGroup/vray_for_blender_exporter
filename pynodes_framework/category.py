# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import nodeitems_utils

class CategoryNodeTree():
    """Node tree that supports categories"""
    @classmethod
    def add_category(cls, name, description="", hint=None, poll=None):
        if poll is None:
            poll = lambda context: True

        class NodeCategory(nodeitems_utils.NodeCategory):
            """Decorator class for categorizing nodes"""

            def __init__(self, name, description="", hint=None):
                def items(context):
                    def item_key(item):
                        # use a/b prefix to ensure unhinted items are sorted alphabetically at the bottom
                        if item[1] is None:
                            return "b%s" % item[0].bl_label
                        else:
                            return "a%s" % str(item[1]).rjust(16)
                    class_list = sorted(self.node_classes, key=item_key)
                    return [ nodeitems_utils.NodeItem(getattr(node_cls, "bl_idname", node_cls.__name__)) for node_cls, _ in class_list ]

                # category names are unique already, can use them for identifier
                super().__init__(identifier=name, name=name, description=description, items=items)
                self.hint = hint
                self.node_classes = set()

            @classmethod
            def poll(category_cls, context):
                space = context.space_data
                return all((space.type == 'NODE_EDITOR', space.tree_type == cls.bl_idname, poll(context)))

            def __call__(self, hint=None):
                def decorate(node_cls):
                    self.node_classes.add((node_cls, hint))
                    return node_cls
                return decorate
 
        # add categories set dynamically, avoids the need for another metaclass
        categories = getattr(cls, "node_categories", None)
        if categories is None:
            categories = {}
            setattr(cls, "node_categories", categories)

        cat = categories.get(name, None)
        if cat is None:
            cat = NodeCategory(name, description, hint)
            categories[name] = cat

        return cat

    @classmethod
    def register_categories(cls):
        categories = getattr(cls, "node_categories", None)
        if categories is None:
            return

        def cat_key(cat):
            # use a/b prefix to ensure unhinted categories are sorted alphabetically at the bottom
            if cat.hint is None:
                return "b%s" % cat.name
            else:
                return "a%s" % str(cat.hint).rjust(16)
        cat_list = sorted(categories.values(), key=cat_key)

        nodeitems_utils.register_node_categories(cls.bl_idname, cat_list)

    @classmethod
    def unregister_categories(cls):
        nodeitems_utils.unregister_node_categories(cls.bl_idname)
