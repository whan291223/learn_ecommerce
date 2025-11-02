Learning how to create the e commerce

Noted 
Fast api flow!

1. model -> SQL model that represent the database table
2. core
|- config.py -> environment variable(database url, env file)
|- db.py -> session -> use by api to complete the request
            |-get session -> 1.create pool of session 2.config those session to database 3.provide method for crud
3. crud -> method for get update delet which will call via "api" file which will get call by "main" too
4. alembic -> make the model.py sync with database
5. main -> contain fastapi server and call "api" in main


chap 8.

Noted

cors -> cross origin Resource sharing
make two domain link together