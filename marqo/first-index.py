import marqo

mq = marqo.Client(url='http://127.0.0.1:8882')

import csv
database_name = "soriee-search"
table_name = database_name
subject = "comics"
with open("../thirdparty/" + subject + ".csv", mode='r') as infile: # https://stackoverflow.com/a/69613250/381724
    reader = csv.DictReader(infile, skipinitialspace=True)
    comics = [r for r in reader]
entries = []
length_of_input = len(comics)
print("Entries: " + str(length_of_input))
current_entry = []
for i in range(length_of_input):
    c = comics[i]
    entry = {
            "title": c["title"], 
            "description": str(c),
            "instruction": "Represent the manga document for retrieval" }
    entries.append(entry)
mq.index(database_name).add_documents(entries, 
    device="cuda", client_batch_size=1000, server_batch_size=1000, processes=4)
results = mq.index(database_name).search(
    q="List some spice and wolf.", searchable_attributes=["title", "description", "instruction"]
)