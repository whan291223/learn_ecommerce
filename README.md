Learning how to create the e commerce

Message 401 when unauthorize mean that may be you didn't send the token yet in front end



Noted 
Fast api flow!

1. model -> SQL model that represent the database table
2. core
|- config.py -> environment variable(database url, env file)
|- db.py -> session -> use by api to complete the request
            |-get session -> 1.create pool of session 2.config those session to database 3.provide method for crud
3. crud -> method for get update delet which will call via "api" file which will get call by "main" too
4. alembic -> make the model.py sync with database
//After made change for models.py need to run

5. main -> contain fastapi server and call "api" in main

podman
- podman machine start
- podman ps -a
- podman image list
- podman pod create --name myapp-pod -p 8000:8000 -p 5173:5173
XXXX podman run -d --pod myapp-pod --name backend -e DATABASE_URL="postgresql+psycopg://postgres:root@postgres:5432/fastapi_ecom" my-fastapi
XXXX podman run -d --pod myapp-pod --name frontend my-react
XXXX podman run -d --pod myapp-pod --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=fastapi_ecom -v "D:\personal_project\prime junction\code goat\db\fastapi_ecom.backup:/backup/fastapi_ecom.backup:Z" postgres:18
- podman exec -it postgres pg_restore -U postgres -d fastapi_ecom /backup/fastapi_ecom.backup                   
- podman run -d --pod myapp-pod --name cloudflared cloudflare/cloudflared:latest tunnel --url http://localhost:5173          
- podman run -d --pod myapp-pod --name frontend -v ".:/app:Z" -v "/app/node_modules" my-react
- podman run -d --pod myapp-pod --name backend -v ".:/app:Z" -e DATABASE_URL="postgresql+psycopg://postgres:root@postgres:5432/fastapi_ecom" my-fastapi
- podman run -d --pod myapp-pod --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=fastapi_ecom -v pgdata:/var/lib/postgresql -v "D:\personal_project\prime junction\code goat\db\fastapi_ecom.backup:/tmp/fastapi_ecom.backup" postgres:18
///////// better dev workflow
backedn
dev image
podman build -t my-fastapi-dev --target dev .
podman run -d --pod myapp-pod --name backend-dev -v ".:/app:Z" -p 5173:5173 dev-fastapi


front end
dev image
podman build -t my-react-dev --target dev .
podman run -d --pod myapp-pod --name frontend-dev -v ".:/app:Z" -p 5173:5173 my-react-dev

pro image
podman build -t my-react-prod --target prod .
podman run -d --pod myapp-pod --name frontend -p 5173:5173 my-react-prod



podman run -d --pod myapp-pod --name postgres-dev -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=fastapi_ecom -v pgdata_dev:/var/lib/postgresql postgres:18















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


-------------
- chap 11
- install httpx
- create new .py file name https.client