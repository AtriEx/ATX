Firstly, make sure you create a .env file in backend/env/.env with the values:
- `PUBLIC_SUPABASE_URL`
- `SUPABASE_KEY`

For more info on the database, [click here](database.md)

**Install FastAPI and Uvicorn using:**
```bash
pip install -r requirements.txt
```

**Run the server using:**
```bash
uvicorn main:app --reload
```
**If the line above doesn't work, try using:**
```bash
python -m uvicorn main:app --reload
```

> [!NOTE]
> Interactive API documentation can be viewed at the /docs url of the server, for example: <br>
> http://127.0.0.1:8000/docs

## Docker
**Build the docker image**
```bash
docker build -t atx .
```

**Run the docker container**
```bash
# Remove -d to start attached to the container
docker run -d -p 8000:8000 atx
```