import marqo

mq = marqo.Client(url='http://127.0.0.1:8882')
results = mq.index("soriee-search").search(
    q="List some spice and wolf.", searchable_attributes=["Title", "Description", "Instruction"]
)
print(results)
