import os

DEFAULTS = {'DB_NAME': 'loadtest',
            'COLLECTION_NAME': 'documents',
            'CLUSTER_URL': f'mongodb+srv://user:password@something.mongodb.net/sample?retryWrites=true&w=majority',
            'DOCS_PER_BATCH': 10,
            'DOC_SIZE': 512,
            'INSERT_WEIGHT': 1,
            'FIND_WEIGHT': 1,
            'BULK_INSERT_WEIGHT': 1,
            'AGG_PIPE_WEIGHT': 1,
            'COLLECTION_SCAN': 'scancoll',
            'SCAN_COLL_FILLSZ_GB': 20,
            # OLTP test related settings
            'OLTP_COLL_FILLSZ_GB': 10,
            'COLLECTION_OLTP': 'oltp',
            }


def init_defaults_from_env():
    for key in DEFAULTS.keys():
        value = os.environ.get(key)
        if value:
            DEFAULTS[key] = value


# get the settings from the environment variables
init_defaults_from_env()
