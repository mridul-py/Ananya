from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from demo import get_connection

app = FastAPI()

class CreateTableRequest(BaseModel):
    table_name: str 
    columns: str

@app.post("/create_table")
def create_table(req: CreateTableRequest):

    sql = f"CREATE TABLE {req.table_name}({req.columns})"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Table created successfully"}