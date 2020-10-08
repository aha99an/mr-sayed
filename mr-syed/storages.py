from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    
    def _get_write_parameters(self, name, content=None):
        params = super()._get_write_parameters(name, content)
        if hasattr(self, 'default_acl'):
            params.update({'ACL': 'public-read'})
        return params
