from clld.web.maps import LanguageMap


class InventoryMap(LanguageMap):
    def get_language(self):
        return self.ctx.language
