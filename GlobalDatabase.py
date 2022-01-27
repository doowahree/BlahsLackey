import os

import psycopg2
from google.protobuf import text_encoding
from psycopg2 import extensions
import threading
import base64

from google.protobuf.message import Message


class _GlobalDatabase(object):
    _instance = None

    def __init__(self):
        print('Initializing global db connection')
        self.db_conn: psycopg2.extensions.connection = psycopg2.connect(os.environ['postgres_database_uri'])
        self._lock = threading.RLock()

    def StoreKeyVal(self, key, val: str = None, val_bytes: bytes = None):
        ret_val = []
        with self._lock:
            with self.db_conn.cursor() as curs:
                c: psycopg2.extensions.cursor = curs
                c.execute("""INSERT INTO key_val
                VALUES(%s, %s, %s)
                ON CONFLICT (key)
                DO
                    UPDATE SET val_str = EXCLUDED.val_str, val_bytes = EXCLUDED.val_bytes;
                """, (key, val or '', val_bytes or bytes()))
                self.db_conn.commit()
        return ret_val

    def LoadKeyVal(self, key):
        ret_val = []
        with self._lock:
            with self.db_conn.cursor() as curs:
                curs.execute("""
                                SELECT *
                                FROM key_val
                                WHERE key = %s;
                                """, (key,))
                ret_val = curs.fetchone()
        return ret_val if ret_val else None

    def StoreProto(self, key, proto: Message):
        ret_val = []
        with self._lock:
            with self.db_conn.cursor() as curs:
                c: psycopg2.extensions.cursor = curs
                c.execute("""INSERT INTO proto_store
                VALUES(%s, %s, %s)
                ON CONFLICT (key_id)
                DO
                    UPDATE SET proto_type = EXCLUDED.proto_type, data = EXCLUDED.data;
                """, (key, proto.DESCRIPTOR.full_name, proto.SerializeToString()))
                self.db_conn.commit()
        return ret_val

    def LoadProto(self, key):
        ret_val = []
        with self._lock:
            with self.db_conn.cursor() as curs:
                curs.execute("""
                        SELECT *
                        FROM proto_store
                        WHERE key_id = %s;
                        """, (key,))
                ret_val = curs.fetchone()
        return bytes(ret_val[2]) if ret_val else None


def GlobalDatabase() -> _GlobalDatabase:
    if not _GlobalDatabase._instance:
        _GlobalDatabase._instance = _GlobalDatabase()
    return _GlobalDatabase._instance
