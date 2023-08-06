from redis import StrictRedis
import sys

sys.path.append('../../')
from inhand.service.SettingService import Redis

class CacheService:
    def __init__(self,settings):
        self.settings = settings

    def connect(self):
        pass

    def close(self):
        pass

    def put(self,key,value,expire=None):
        raise (NameError, "Unsupported!")

    def get(self, key):
        raise (NameError, "Unsupported!")

    def exists(self, key):
        raise (NameError, "Unsupported!")

    @staticmethod
    def createCacheService(settings):
        if isinstance(settings,Redis):
            return RedisCacheService(settings)
            raise (NameError, "Unsupported cache type: {}".format(database.type))

class RedisCacheService(CacheService):

    def __init__(self,settings):
        super().__init__(settings)
        self.cache=StrictRedis(host=settings.host,
                             port=settings.port,
                             db=settings.database,
                             password=settings.password)
