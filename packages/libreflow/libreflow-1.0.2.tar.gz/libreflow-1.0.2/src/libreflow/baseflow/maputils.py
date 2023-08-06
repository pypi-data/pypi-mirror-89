import os
import shutil
import re

from kabaret import flow


class CreateGenericItemAction(flow.Action):
    """
    Creates an item with a generic key.

    This class may be parented to a *GenericMap* (or subclass),
    which provides items prefix and index format padding to
    define their keys in the map.
    """
    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    _map = flow.Parent()

    def get_buttons(self):
        item_class_name = self._map.mapped_type().__name__.lower()
        self.message.set("<h2>Create %s</h2>" % item_class_name)

        return ['Create', 'Cancel']

    def needs_dialog(self):
        return False

    def run(self, button):
        if button == 'Cancel':
            return

        map_size = len(self._map)
        name = '{prefix}{item_index:0{padding}d}'.format(
            prefix=self._map.item_prefix,
            item_index=map_size,
            padding=self._map.item_padding
        )
        item = self._map.add(name)

        self._map.touch()

        return item


class SimpleCreateAction(CreateGenericItemAction):
    """
    This is a simple create action for maps. It's usefull only for
    simple creations with just the name of the object.
    You should create a custom create action if you need more information
    """

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    entity_name = flow.Param('').ui(label='Name')

    def needs_dialog(self):
        return True

    def run(self, button):
        if button == 'Cancel':
            return

        if self.entity_name.get() == "":
            msg = self.message.get()
            msg += "<font color=#D5000D>%s name must be not empty.</font>" % self._map.mapped_type().__name__.lower()
            self.message.set(msg)

            return self.get_result(close=False)

        self._map.add(self.entity_name.get())
        self._map.touch()


class CreateItemAction(CreateGenericItemAction):
    """
    Adds to a map an item containing a description param.
    """
    description = flow.Param('')

    def needs_dialog(self):
        return True

    def run(self, button):
        if button == 'Cancel':
            return

        super(CreateItemAction, self).run(button)
        item = self._map.mapped_items()[-1]
        item.description.set(self.description.get())

        self._map.touch()


class ClearMapAction(flow.Action):
    """
    Clears all map's items.
    """
    ICON = ('icons.gui', 'remove-symbol')

    _map = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        self._map.clear()
        self._map.touch()


class GenericItemMap(flow.Map):
    """
    A map defining attributes used to index items generically.

    An item's key is made of a prefix (*item_prefix*) and the item's
    index formatted according to a padding number (*item_padding*).
    Subclasses may provide a relation to a *CreateGenericItemAction*
    (or subclass) making use of these attributes.
    """
    item_prefix = 'prefix_'
    item_padding = 3


class ItemMap(GenericItemMap):
    """
    A map composed of items with a description.
    """
    def columns(self):
        return ['Name', 'Description']

    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()
        row["Description"] = item.description.get()
