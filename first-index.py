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

import marqo

mq = marqo.Client(url='http://127.0.0.1:8882')

import csv
database_name = "soriee-search"
table_name = database_name
subject = "games"
with open("../thirdparty/" + subject + ".csv", mode='r') as infile: # https://stackoverflow.com/a/69613250/381724
    reader = csv.DictReader(infile, skipinitialspace=True)
    games = [r for r in reader]
entries = []
length_of_input = len(games)
print("Entries: " + str(length_of_input))
current_entry = []
for i in range(length_of_input):
    c = games[i]
    entry = {
                "AppID": c["AppID"],
                "Name": c["Name"], 
                "Release date": c["Release date"],
                "Estimated owners": c["Estimated owners"],
                "Peak CCU": c["Peak CCU"],
                "Required age": c["Required age"],
                "Price": c["Price"],
                "DLC count": c["DLC count"],
                "About the game": c["About the game"],
                "Supported languages": c["Supported languages"],
                "Full audio languages": c["Full audio languages"],
                "Reviews": c["Reviews"],
                "Header image": c["Header image"],
                "Website": c["Website"],
                "Support url": c["Support url"],
                "Support email": c["Support email"],
                "Windows": c["Windows"],
                "Mac": c["Mac"],
                "Linux": c["Linux"],
                "Metacritic score": c["Metacritic score"],
                "Metacritic url": c["Metacritic url"],
                "User score": c["User score"],
                "Positive": c["Positive"],
                "Negative": c["Negative"],
                "Score rank": c["Score rank"],
                "Achievements": c["Achievements"],
                "Recommendations": c["Recommendations"],
                "Notes": c["Notes"],
                "Average playtime forever": c["Average playtime forever"],
                "Average playtime two weeks": c["Average playtime two weeks"],
                "Median playtime forever": c["Median playtime forever"],
                "Median playtime two weeks": c["Median playtime two weeks"],
                "Developers": c["Developers"],
                "Publishers": c["Publishers"],
                "Categories": c["Categories"],
                "Genres": c["Genres"],
                "Tags": c["Tags"],
                "Screenshots": c["Screenshots"],
                "Movies": c["Movies"],
                "Instruction": "Represent the game document for retrieval"
            }
    entries.append(entry)
mq.index(database_name).add_documents(entries, 
    device="cuda", client_batch_size=100, processes=4)
results = mq.index(database_name).search(
    q="List some spice and wolf.", searchable_attributes=["Source", "Instruction","AppID","Name","Release date","Estimated owners","Peak CCU","Required age","Price","DLC count","About the game","Supported languages","Full audio languages","Reviews","Header image","Website","Support url","Support email","Windows","Mac","Linux","Metacritic score","Metacritic url","User score","Positive","Negative","Score rank","Achievements","Recommendations","Notes","Average playtime forever","Average playtime two weeks","Median playtime forever","Median playtime two weeks","Developers","Publishers","Categories","Genres","Tags","Screenshots,Movies"]
)