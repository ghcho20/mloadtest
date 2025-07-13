from locust import between
import inspect, random, time, bson

from utils import gen_docs
from datetime import datetime, timezone
from bson.objectid import ObjectId

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
    sweight = 0
    if 0 == rweight and 0 == wweight:
        wweight = 1
        sweight = 1

    print(f'Config: doc_size={doc_size}, docs_per_batch={docs_per_batch}, rweight={rweight}, wweight={wweight}, sweight={sweight}')
    return (doc_size, docs_per_batch, rweight, wweight, sweight)

class TestUser(MongoUser):
    """
    User class for load testing MongoDB operations.
    """
    wait_time = between(0.0, 0.0)
    doc_size, docs_per_batch, rweight, wweight, sweight = init_config()


    def __init__(self, environment):
        super().__init__(environment)

    def on_start(self):
        """
        Initialize the user by connecting to the MongoDB cluster.
        """
        # if DEFAULTS['COLLECTION_NAME'] in self.db.list_collection_names():
        #     self.db.drop_collection(DEFAULTS['COLLECTION_NAME'])
        self.coll, _ = self.ensure_collection(DEFAULTS['COLLECTION_NAME'])

        self.start_time = datetime.now(timezone.utc)

    @mongodb_task(weight=rweight)
    def find(self):
        cur_time = datetime.now(timezone.utc)
        inbetween = between(self.start_time.timestamp(), cur_time.timestamp())(None)
        inbetween_oid = ObjectId.from_datetime(datetime.fromtimestamp(inbetween, tz=timezone.utc))
        found_one = self.coll.find_one({'_id': {'$gt': inbetween_oid}})
        return len(bson.BSON.encode(found_one))

    @mongodb_task(weight=wweight)
    def bulk_insert(self):
        doc_size = self.doc_size if self.doc_size > 0 else random.choice([512, 1024, 10240, 102400])
        docs_batch = gen_docs(doc_size, self.docs_per_batch)
        self.coll.insert_many(docs_batch)
        return len(bson.BSON.encode(docs_batch[0])) * self.docs_per_batch

class ScanUser(MongoUser):
    """
    User class for performing collection scans in MongoDB.
    """
    wait_time = between(0.0, 0.0)
    doc_size, docs_per_batch, rweight, wweight, sweight = init_config()
    fixed_count = 1

    def __init__(self, environment):
        super().__init__(environment)

    def on_start(self):
        """
        Initialize the user by connecting to the MongoDB cluster.
        """
        self.coll, _ = self.ensure_collection(DEFAULTS['COLLECTION_SCAN'])

    @mongodb_task(weight=sweight)
    def scan(self):
        finds = self.coll.find() # collection scan
        len_docs = 0
        for f in finds: 
            len_docs += len(bson.BSON.encode(f))
            time.sleep(0)
        return len_docs