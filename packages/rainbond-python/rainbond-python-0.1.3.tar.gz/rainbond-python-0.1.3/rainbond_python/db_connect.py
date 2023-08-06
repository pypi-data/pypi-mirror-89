import os
import pymongo
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


class DBConnect():
    def __init__(self, db, collection, home_kye='MONGODB_HOST', port_kye='MONGODB_PORT'):
        self.mongo_home = os.environ.get(home_kye, None)
        self.mongo_port = os.environ.get(port_kye, 27017)

        if not self.mongo_home or not self.mongo_port:
            logging.error('MongoDB(组件)的组件连接信息是不完整的')

        self.mongo_client = pymongo.MongoClient(
            host=self.mongo_home,
            port=int(self.mongo_port)
        )
        self.mongo_db = self.mongo_client[db]
        self.mongo_collection = self.mongo_db[collection]

    def get_collection(self):
        return self.mongo_collection

    def write_one_docu(self, docu):
        try:
            self.mongo_collection.insert_one(docu)
            return True
        except Exception as err:
            logging.warning('MongoDB(组件)出现未知错误: {0}'.format(err))
            return False
