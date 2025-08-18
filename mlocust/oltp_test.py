from locust import between
import inspect, random, time, bson

from utils import gen_docs
from datetime import datetime, timezone

from settings import DEFAULTS
from mongo_user import MongoUser, mongodb_task

def init_config():
    """
    Initialize configuration settings for the load test.
    """
    doc_size = int(DEFAULTS['DOC_SIZE'])
    docs_per_batch = int(DEFAULTS['DOCS_PER_BATCH'])
    rweight = int(DEFAULTS['FIND_WEIGHT'])
    wweight = int(DEFAULTS['BULK_INSERT_WEIGHT'])

    print(f'Config: doc_size={doc_size}, docs_per_batch={docs_per_batch}, rweight={rweight}, wweight={wweight}')
    return (doc_size, docs_per_batch, rweight, wweight)

class TestUser(MongoUser):
    """
    User class for load testing MongoDB operations.
    """
    wait_time = between(0.0, 0.0)
    doc_size, docs_per_batch, rweight, wweight = init_config()


    def __init__(self, environment):
        super().__init__(environment)

    def on_start(self):
        """
        Initialize the user by connecting to the MongoDB cluster.
        """
        # if DEFAULTS['COLLECTION_NAME'] in self.db.list_collection_names():
        #     self.db.drop_collection(DEFAULTS['COLLECTION_NAME'])
        self.coll, _ = self.ensure_collection(DEFAULTS['COLLECTION_NAME'])

    @mongodb_task(weight=rweight)
    def find(self):
        filters = random.sample(range(1, 65_536), 2)
        docs = list(self.coll.find({'filter': {'$in': filters}}))
        return 4*1024*len(docs) if docs else 0

    @mongodb_task(weight=wweight)
    def bulk_insert(self):
        docs_batch = gen_docs(self.doc_size, self.docs_per_batch)
        self.coll.insert_many(docs_batch)
        return len(bson.BSON.encode(docs_batch[0])) * self.docs_per_batch
