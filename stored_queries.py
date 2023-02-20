import csv
from sqlite_utils.utils import sqlite3
from sqlite_utils import Database
database_name = "soriee-search"
table_name = "query"

db = Database(database_name + ".db")
table_name = "saved_queries"
try:
    db[table_name].create({
        "name": str,
        "sql": str,
        "author_id": str,
    }, pk="name", )        
except sqlite3.OperationalError:
    pass
try:
    db["saved_queries"].insert({
        "name": "Find similar documents by combining regular search and embedding search.",
        "sql": """
    with related as (
    select
        value
    from
        json_each(
        faiss_search(
            "soriee-search",
            "soriee-search",
            (
            select
                embedding
            from
                "soriee-search"
            where
                source like "%'Trapped in a Video Game'%"
            limit
                1
            ), 10
        )
        )
    )
    select
    prompt
    from
    "soriee-search",
    related
    where
    id = value
        """
    }, replace=True)        
except sqlite3.OperationalError:
    pass