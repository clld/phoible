from clld.web.adapters import GeoJsonParameter


class GeoJsonFeature(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {}
