import marqo

mq = marqo.Client(url='http://127.0.0.1:8882')
index = "soriee-search"
results = mq.index(index).get_stats()
print(results)