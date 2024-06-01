import pickle

# Example keys to store in the pickled database
keys_db = {
    "key1": "some_value1",
    "key2": "some_value2",
    "key3": "some_value3"
}

# Save the keys to a pickle file
with open('keys_db.pkl', 'wb') as f:
    pickle.dump(keys_db, f)
