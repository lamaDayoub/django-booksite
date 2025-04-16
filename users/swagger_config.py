from drf_yasg.inspectors import SwaggerAutoSchema

class ForceMethodsSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys):
        if 'api' in operation_keys and 'token' in operation_keys:
            return ['Authentication']
        return super().get_tags(operation_keys)
    
    def should_filter(self):
        """Force inclusion of all methods"""
        return False