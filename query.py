import csv
from sqlite_utils.utils import sqlite3
from sqlite_utils import Database
from InstructorEmbedding import INSTRUCTOR
model = INSTRUCTOR('hkunlp/instructor-xl')

database_name = "soriee-search"
table_name = "query"

db = Database(database_name + ".db")
try:
    db[table_name].drop()
    db[table_name].create({
        "id": str,
        "embedding":  "BLOB",
        "source":  "BLOB",
        "instruction": str,
        "prompt": str,
    }, pk="id", )
    db[table_name].create_index(["id"], unique=True)
    db[table_name].create_index(["source"], unique=True)
except sqlite3.OperationalError:
    pass

import struct
def encode(vector):
    return struct.pack("f" * len(vector), *vector)

current_entry = ["Represent manga question for document retrieval: ", "What is a vrmmorpg?"]
length_of_input = len(current_entry)
print("Entries: " + str(length_of_input))
from uuid_extensions import uuid7
import datetime
# Time the buckets to be 15 seconds maximum.
count = 0
embeddings = model.encode(current_entry)
bucket_size = len(current_entry)
source = []
id = uuid7()
instruction = current_entry[0]
source = current_entry[1]
prompt = current_entry[1]
try:
    db[table_name].insert({"id": id, "embedding": encode(embeddings[0]), "instruction": instruction, "prompt": prompt, "source": source}, pk="id", replace=True)
except sqlite3.IntegrityError:
    print("Record already exists with that primary key")
prompt = """tags: ['Action', 'Adventure', 'Comedy', 'Manhwa', 'Webtoons', 'Full Color', 'MMORPG', 'RPG', 'Virtual Reality', 'Based on a Web Novel']"""
source = prompt
try:
    db[table_name].insert({"id": id, "embedding": encode(embeddings[0]), "instruction": instruction, "prompt": prompt, "source": source}, pk="id", replace=True)
except sqlite3.IntegrityError:
    print("Record already exists with that primary key")
