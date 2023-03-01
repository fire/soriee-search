import marqo

database_name = "soriee-search"
mq = marqo.Client(url='http://127.0.0.1:8882')
mq.index(database_name).delete()