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
bucket_size = round(float(length_of_input) / 200)
for i in range(length_of_input):
    c = comics[i]
    id = c["title"]
    entry = {
            "Title": c["title"], 
            "Description": c,
            "Instruction": "Represent the manga document for retrieval" }
    entries.append(entry)
mq.index("soriee-search").add_documents(entries)
