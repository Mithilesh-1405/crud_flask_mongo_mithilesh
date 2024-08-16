db = db.getSiblingDB("crud_db");
db.crud_db.drop();

db.crud_db.insertMany([
    {
        "id": 1,
        "name": "user1",
        "email": "user1@gmail.com",
        "password": "user1"

    },
    {
        "id": 2,
        "name": "user2",
        "email": "user2@gmail.com",
        "password": "user2"
    },

]);