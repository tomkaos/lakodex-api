from lakodex_api.apps.core.renderers import LakodexJSONRenderer


class ProfileJSONRenderer(LakodexJSONRenderer):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'
