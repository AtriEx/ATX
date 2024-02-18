**Install FastAPI and Uvicorn using:**
```bash
pip install -r requirements.txt
```

**Run the server using:**
```bash
uvicorn main:APP --reload
```
**If the line above doesn't work, try using:**
```bash
python -m uvicorn main:APP --reload
```

> [!NOTE]
> Interactive API documentation can be viewed at the /docs url of the server, for example: <br>
> http://127.0.0.1:8000/docs
