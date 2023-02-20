import csv
from sqlite_utils.utils import sqlite3
from sqlite_utils import Database
from InstructorEmbedding import INSTRUCTOR
model = INSTRUCTOR('hkunlp/instructor-xl')
database_name = "soriee-search"
table_name = database_name
subject = "comics"
with open("thirdparty/" + subject + ".csv", mode='r') as infile: # https://stackoverflow.com/a/69613250/381724
    reader = csv.DictReader(infile, skipinitialspace=True)
    comics = [r for r in reader]
db = Database(database_name + ".db")
try:
    db[table_name].create({
        "id": str,
        "embedding":  "BLOB",
        "source":  "BLOB",
        "instruction": str,
        "prompt": str,
    }, pk="id")
    db[table_name].create_index(["id"], unique=True)
    db[table_name].create_index(["source"], unique=True)
except sqlite3.OperationalError:
    pass
import struct
def encode(vector):
    return struct.pack("f" * len(vector), *vector)
entries = []
ids = []
length_of_input = len(comics)
print("Entries: " + str(length_of_input))
current_entry = []
bucket_size = round(float(length_of_input) / 200)
for i in range(length_of_input):
    c = comics[i]
    id = c["title"]
    ids.append(id)
    entry = ["Represent the manga document for retrieval: ", "title: " + c["title"] + " description: " + c["description"] + " year: " + c["year"] + " tags: " + c["tags"], c]
    current_entry.append(entry)
    if i % bucket_size == 0: 
        entries.append(current_entry)
        current_entry = []
import datetime
print(datetime.datetime.now().isoformat()) # Time the buckets to be 15 seconds maximum.
count = 0
from uuid_extensions import uuid7
for bucket in entries:
    embeddings = model.encode(bucket)
    bucket_size = len(bucket)
    instruction = ""
    prompt = ""
    source = []
    queries = []
    for bucket_i in range(bucket_size):
        instruction = bucket[bucket_i][0]
        prompt = bucket[bucket_i][1]
        source = bucket[bucket_i][2]
        queries.append({"id": uuid7(), "embedding": encode(embeddings[bucket_i]), "instruction": instruction, "prompt": prompt, "source": source})
    try:
        db[table_name].insert_all(queries, pk="id")
    except sqlite3.IntegrityError:
        print("Record already exists with that primary key")
    print(datetime.datetime.now().isoformat() + " " + str(count) + "/" + str(length_of_input))
    count = count + bucket_size
