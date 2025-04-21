# Paradocx
AI search for Paragon's Mintlify docs
## Running Locally
### Starting backend
`fastapi dev fastapi-paradocx/main.py`
### Starting frontend
`npm run start`

## Docker for Fastapi
1) Run `docker build -t fastapi-paradocx .`
2) Run `docker run -d --name fastapi-paradocx -p 80:80 --env-file .env fastapi-paradocx`
