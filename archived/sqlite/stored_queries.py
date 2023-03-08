# MIT License

# Copyright (c) 2023-present K. S. Ernest (iFire) Lee

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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