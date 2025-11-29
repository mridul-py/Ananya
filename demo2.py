from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from demo import get_connection

app = FastAPI()

class sql_queryRequest(BaseModel):
    query : str

@app.post("/run_query")
def run_query(req: sql_queryRequest):
    sql = req.query

    clean_query = sql.strip().lower()

    if clean_query.startswith("select"):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            raise HTTPException(status_code = 400, detail = str(e))
        finally:
            cursor.close()
            conn.close()
        return {"data" : data}
    
    elif clean_query.startswith(("insert", "update", "delete")):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            conn.commit()
            data = {"rows.affected" : cursor.rowcount}
        except Exception as e:
            raise HTTPException(status_code = 400, detail = str(e))
        finally:
            cursor.close()
            conn.close()
        return {"data" : data}
    
    elif clean_query.startswith(("create", "drop", "alter")):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code = 400, detail = str(e))
        finally:
            cursor.close()
            conn.close()
        return {"message" : "Query executed successfully"}
    
    else:

        raise HTTPException(status_code = 400, detail = "Unsupported query type")
     

   


        
