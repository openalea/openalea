import inspect


class UnknownItemError(Exception):
    pass


def get_criteria(plugin):
    criteria = {}
    for criterion in dir(plugin):
        if criterion.startswith('_'):
            continue
        elif criterion in ('implementation', 'name_conversion', 'identifier', 'tags', 'criteria'):
            continue
        criteria[criterion] = getattr(plugin, criterion)
    return criteria


class GenericManager(object):

    def __init__(self, items=None, item_proxy=None, autoload=['entry_points']):
        """
        :param plugins: list of plugins you want to add manually
        :param plugin_proxy: proxy class to use by default
        """
        self._autoload = autoload
        self.default_group = 'default'

        self._item = {}  # dict group -> item name -> item class or item proxy
        self._item_proxy = {}

        self.debug = False
        self._proxies = {}

        self.item_proxy = item_proxy

        if items is not None:
            self.add_items(items)

    # API TO IMPLEMENT

    def generate_item_id(self):
        raise NotImplementedError

    def load_items(self, group=None):
        raise NotImplementedError

    def discover(self, group=None):
        raise NotImplementedError

    # API COMMON TO ALL MANAGERS

    def generate_item_name(self, item):
        try:
            name = item.name
        except AttributeError:
            try:
                name = item.__class__.__name__
            except AttributeError:
                name = str(item.__class__)
        return name

    def clear(self):
        self._item = {}  # dict group -> item name -> item class or item proxy
        self._item_loaded = {}
        self._proxies = {}

    def add(self, item, group, item_proxy=None, **kwds):
        if item_proxy is None and group in self._item_proxy:
            item_proxy = self._item_proxy[group]

        if item_proxy:
            item = item_proxy(item)

        if inspect.isclass(item):
            item = item()
        else:
            raise NotImplementedError

        self.patch_item(item)
        self._item.setdefault(group, {})[item.identifier] = item
        return item

    def add_items(self, items, group):
        for group, item in items.iteritems():
            self.add(item, group)

    def item(self, identifier, group=None):
        """
        item(self, group, identifier)
        -> Plugin or raises UnknownPluginError
        """
        if group is None:
            group = self.default_group
        items = self.items(group)
        if identifier in self._item[group]:
            return self._item[group][identifier]
        else:
            for item in items:
                if item.name == identifier:
                    return item
            args = dict(identifier=identifier, group=group)
            raise UnknownItemError("Item %(identifier)s not found in %(group)s" % args)

    def items(self, group=None, tags=None, criteria=None, **kwds):
        if group is None:
            return self.default_group
        try:
            items = self._item[group].values()
        except KeyError:
            self._item.setdefault(group, {})
            self.discover(group)
            items = self._item[group].values()

        if criteria is None:
            criteria = {}

        valid_items = []
        for pl in items:
            # Check tags. If one tag dont match, ignore this item
            if tags is not None and all(tag in pl.tags for tag in tags) is False:
                continue

            # Check all criteria. If one criteria dont match, ignore item
            if not all(hasattr(pl, criterion) and getattr(pl, criterion)
                       == criteria[criterion] for criterion in criteria):
                continue

            valid_items.append(pl)

        return valid_items

    def patch_item(self, item):
        if hasattr(item, '__patched__'):
            return
        item.__patched__ = True
        item.__class__.criteria = property(fget=get_criteria)
        if not hasattr(item, "identifier"):
            item.identifier = self.generate_item_id(item)
        if not hasattr(item, "name"):
            item.name = self.generate_item_name(item)
        if not hasattr(item, "label"):
            item.label = item.name.replace('_', ' ').capitalize()
        if not hasattr(item, "tags"):
            item.tags = []

        item.__class__.criteria = property(fget=get_criteria)

    def set_proxy(self, group, item_proxy):
        """
        Embed all item for given group in item_proxy.
        """
        self._item_proxy[group] = item_proxy

    def _sorted_items(self, items):
        item_dict = {}
        for item in items:
            item_dict[item.name] = item
        sorted_items = [item_dict[name] for name in sorted(item_dict.keys())]
        return sorted_items
