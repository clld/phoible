from clld.web.maps import LanguageMap, Map, ParameterMap


class LanguagesMap(Map):
    def get_options(self):
        return {'icon_size': 20}


class SegmentMap(ParameterMap):
    def get_options(self):
        return {'icon_size': 20}


class InventoryMap(LanguageMap):
    def get_options(self):
        return {'icon_size': 20}

    def get_language(self):
        return self.ctx.language


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', SegmentMap)
    config.register_map('contribution', InventoryMap)
