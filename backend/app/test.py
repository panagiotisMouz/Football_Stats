from app.database import SessionLocal
from sqlalchemy import text

def run_query(query_str):
    session = SessionLocal()
    try:
        result = session.execute(text(query_str))
        columns = result.keys()
        rows = result.fetchall()

        print(" Query results:")
        print(" | ".join(columns))
        for row in rows:
            print(" | ".join(str(v) for v in row))

    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        session.close()



query = """
        SELECT * FROM view_top_scorers LIMIT 10;
    """
run_query(query)


