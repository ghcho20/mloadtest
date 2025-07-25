import os

DEFAULTS = {'DB_NAME': 'loadtest',
            'COLLECTION_NAME': 'documents',
            'CLUSTER_URL': f'mongodb+srv://user:password@something.mongodb.net/sample?retryWrites=true&w=majority',
            'DOCS_PER_BATCH': 100,
            'DOC_SIZE': 512,
            'INSERT_WEIGHT': 1,
            'FIND_WEIGHT': 3,
            'BULK_INSERT_WEIGHT': 1,
            'AGG_PIPE_WEIGHT': 1,
            'COLLECTION_SCAN': 'scancoll',
            'SCAN_COLL_FILLSZ_GB': 20,
            }


def init_defaults_from_env():
    for key in DEFAULTS.keys():
        value = os.environ.get(key)
        if value:
            DEFAULTS[key] = value


# get the settings from the environment variables
init_defaults_from_env()
