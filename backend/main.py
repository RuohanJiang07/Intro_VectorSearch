from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from vector_search import schematic_search
import sqlite3
import numpy as np

app = FastAPI(title="Search API (Vector + Traditional)")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    Name: str
    Category: str
    Label: str
    Profile_Chunk: str
    Similarity: Optional[float] = None


# VECTOR SEARCH ENDPOINT
@app.post("/api/search")
async def vector_search(query: SearchQuery) -> List[dict]:
    try:
        results = schematic_search(query.query)
        if results.empty:
            return []
        
        results_list = results.to_dict('records')
        
        for result in results_list:
            result['Similarity'] = float(min(max(result.get('Similarity', 0.0), 0.0), 1.0))
            for key, value in result.items():
                if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                    result[key] = 0.0
        
        return results_list
    except Exception as e:
        print(f"Vector Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# TRADITIONAL SEARCH ENDPOINT
@app.post("/api/traditional_search")
async def traditional_search(query: SearchQuery) -> List[dict]:
    DB_PATH = './data/experts.db'

    if not query.query.strip():
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # SQL Search Query
        search_query = """
        SELECT name AS Name, category AS Category, label AS Label, profile AS Profile_Chunk, url AS URL
        FROM expert_profiles
        WHERE name LIKE ?
        OR label LIKE ?
        OR profile LIKE ?
        """
        
        cursor.execute(search_query, (f'%{query.query}%', f'%{query.query}%', f'%{query.query}%'))
        rows = cursor.fetchall()
        conn.close()
        
        # Format results
        results = []
        for row in rows:
            results.append({
                "Name": row["Name"],
                "Category": row["Category"],
                "Label": row["Label"],
                "Profile_Chunk": row["Profile_Chunk"],
                "URL": row["URL"]
            })
        
        return results
    
    except Exception as e:
        print(f"Traditional Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
