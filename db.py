import pymongo

# setup
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['ai_bc_db'] # AI Boot camp Database lol
history_col = db['history'] # History collection


# db CRUD functions
def insert_one_to_db(d: dict):
    res = history_col.insert_one(d)
    print(f"Document {res.inserted_id} added!")

def get_all():
    return list(history_col.find())

def find_data_by_id(video_id: str):
    res = history_col.find_one({"_id": video_id})

    return res