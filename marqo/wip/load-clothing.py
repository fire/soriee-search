import os
import requests
import pandas as pd
from PIL import Image
import pprint
import marqo

database_name = "clothing-dataset"
mq = marqo.Client(url='http://127.0.0.1:8882') # Connection to Marqo Docker Container
cwd = os.getcwd() # Get current working directory
shirt_data = pd.read_csv('clothing-dataset/images.csv')[['image','label','kids']].to_dict('records')

for data in shirt_data:
    path = "http://127.0.0.1:8222/clothing-dataset/images/" + data['image'] + ".jpg"
    data['image'] = path

settings = {
    "index_defaults": {
        "treat_urls_and_pointers_as_images":True,   # allows us to find an image file and index it
        "image_preprocessing": {
            "patch_method": "overlap"
        },
        "model":"onnx16/open_clip/ViT-H-14/laion2b_s32b_b79k",
        "normalize_embeddings":True,
    }
}
mq.index(database_name).delete()
mq.create_index(database_name, settings_dict=settings)
mq.index(database_name).add_documents(shirt_data)