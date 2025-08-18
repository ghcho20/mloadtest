from settings import DEFAULTS
from utils import gen_docs_gb
import pymongo
import threading, queue, time

def fillup_collection(coll_name):
    """
    Fill up the collection with random documents
    """
    try:
        client = pymongo.MongoClient(DEFAULTS['CLUSTER_URL'])
        db = client[DEFAULTS['DB_NAME']]

        if coll_name in db.list_collection_names():
            db.drop_collection(coll_name)
        db.create_collection(coll_name)

        collection = db.get_collection(coll_name)
        collection.create_index([('filter', pymongo.ASCENDING)])

        total_size_gb = float(DEFAULTS['OLTP_COLL_FILLSZ_GB'])
        NUM_THREADS = 8  # Number of threads to use for generating documents
        print(f"Generating documents to fill {coll_name} with {total_size_gb} GB of data...")

        result_queue = queue.Queue()
        def worker(work_id: int, total_size_gb: float, doc_size: int, batch_size: int):
            print(f"Worker {work_id} started")
            nDocs = 0
            for docs in gen_docs_gb(total_size_gb, doc_size, batch_size):
                collection.insert_many(docs)
                nDocs += len(docs)
                print(f"Worker {work_id} inserted {nDocs} documents")
            result_queue.put((work_id, nDocs))

        threads = []
        for i in range(1, NUM_THREADS+1):
            thread = threading.Thread(target=worker, args=(i, total_size_gb/NUM_THREADS, 2*1024, 500))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    finally:
        client.close()

    total_docs = 0
    while not result_queue.empty():
        work_id, nDocs = result_queue.get()
        total_docs += nDocs
        print(f"Worker {work_id} finished with {nDocs} documents")

    print(f"Collection {coll_name} filled with {total_docs} documents.")

if __name__ == "__main__":
    coll_name = DEFAULTS['COLLECTION_OLTP']

    start_time = time.time()
    try:
        fillup_collection(coll_name)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"Completed in {duration:.2f} seconds.")