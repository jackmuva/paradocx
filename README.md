# Paradocx
AI search for Paragon's Mintlify docs
## Running Locally
### Starting backend
* Install dependencies with `pip install fastapi-paradocx/requirements.txt`
* Set env vars by creating a `.env` file with the contents
```
PINECONE_API_KEY=
PINECONE_DENSE_INDEX=paradocx-dense-index
PINECONE_SPARSE_INDEX=paradocx-sparse-index
PINECONE_NAMESPACE=paradocx-dev

#Paragon OpenAI Key
OPENAI_API_KEY=
TOKENIZERS_PARALLELISM=false

ABSOLUTE_PATH_TO_DOCS="/Users/PATH_TO_MINTLIFY_DOCS"
```
* Run server locally `fastapi dev fastapi-paradocx/main.py`
### Starting frontend
* Install dependencies with `npm install`
* Run `npm run start`

## Docker for Fastapi
1) Run `docker build -t fastapi-paradocx .`
2) Run `docker run -d --name fastapi-paradocx -p 80:80 --env-file .env fastapi-paradocx`
