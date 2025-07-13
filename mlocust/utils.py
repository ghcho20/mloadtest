from faker import Faker
import bson

def gen_doc(doc_size: int):
    """
    Generate a random document with a specified size.
    :param doc_size: size of the document in bytes
    :return: a dictionary representing the document
    """
    fake = Faker()
    doc = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'text': fake.text(),
        'pad': ''
    }
    pad_size = doc_size - len(bson.BSON.encode({'_id': bson.objectid.ObjectId(), **doc}))
    doc['pad'] = 'p' * pad_size if pad_size > 0 else ''
    return doc

def gen_docs(doc_size: int, batch_size: int):
    """
    Generate a list of random documents
    :param doc_size: size of each document in bytes
    :param batch_size: number of documents to yield at once
    :return: lists of documents
    """
    return [gen_doc(doc_size) for _ in range(batch_size)]

def gen_docs_gb(total_size_gb: float, doc_size: int, batch_size: int):
    """
    Generate a list of random documents
    :param total_size_gb: total size of documents to generate in GB
    :param doc_size: size of each document in bytes
    :param batch_size: number of documents to yield at once
    :return: generator yielding lists of documents
    """
    total_size = int(1024**3 * total_size_gb)  # total size in bytes
    
    for _ in range(total_size // (doc_size * batch_size)):
        yield gen_docs(doc_size, batch_size)
