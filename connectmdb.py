from pymongo import *
class Connectmdb(object):
    instance=None
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance=super().__new__(cls)
        return cls.instance
    def __init__(self,hostname='localhost',port=27014,database='myclass'):
        if not isinstance(hostname,str) and isinstance(port,int):
            raise TypeError('invalid hostname','invalid port')
        self._client = MongoClient(hostname, port)
        if not isinstance(database,str):
            raise TypeError('invalid database')
        self._db=self._client[database]
        if self._db.list_collection_names(session=None):
            print('Connect sucessfully with %s !'%database)
            self._hostname = hostname
            self._port = port
            self._database = database
        else:
            raise TimeoutError('connection refused!')
    def disconnectmdb(self):
        return self._client.close()



