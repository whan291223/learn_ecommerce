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

chap 10
 🔐 LOGIN PHASE
┌──────────────────────────────────────────────────────────┐
│ 1. User sends username + password to /users/token        │
│                                                          │
│   POST /users/token                                      │
│   { "username": "alice", "password": "1234" }            │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│ 2. Server checks password                                │
│                                                          │
│ If OK → create_access_token({ "sub": "alice" })          │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│ 3. Server returns JWT token                              │
│                                                          │
│ { "access_token": "<jwt_here>", "token_type": "bearer" } │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
          🧍 User now holds a signed JWT "identity card"


               🔓 USING PROTECTED ENDPOINTS
User wants to GET /products
User sends:

GET /products
Authorization: Bearer <jwt_here>
🔍 Behind The Scenes (get_current_user)

┌─────────────────────────────────────────────┐
│ FastAPI reads token using oauth2_schema     │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ get_current_user receives the token         │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 1. Decode JWT                               │
│    payload = jwt.decode(token, SECRET_KEY)  │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 2. Extract "sub" → username                 │
│    username = payload["sub"]                │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 3. Lookup user in the database              │
│    user = get_user_by_username(username)    │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 4. If user exists → return user             │
│    else → 401 unauthorized                  │
└─────────────────────────────────────────────┘

------------------------------------------------------------
🧀 Final Flow (Simplified)

Login → Server gives JWT (contains "sub" = username)
       ↓
User keeps JWT
       ↓
User calls protected route with JWT
       ↓
Server verifies JWT + reads "sub"
       ↓
Server loads user from DB
       ↓
Access granted ✔️