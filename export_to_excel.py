import psycopg2
import pandas as pd
import os

def export_queries():
    conn = psycopg2.connect(
        dbname="dvdrental",
        user="postgres",
        password="root",
        host="localhost"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    any_failed = False
    
    excel_path = "sql_exercise_outputs.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for i in range(1, 15):
            filepath = f"task{i}.sql"
            if not os.path.exists(filepath):
                print(f"File {filepath} not found.")
                continue
                
            with open(filepath, 'r') as f:
                sql_content = f.read()
                
            statements = sql_content.split(';')
            
            for stmt in statements:
                lines = stmt.split('\n')
                clean_lines = [line for line in lines if not line.strip().startswith('--')]
                clean_stmt = '\n'.join(clean_lines).strip()
                
                if not clean_stmt:
                    continue
                    
                try:
                    cur.execute(clean_stmt)
                    if cur.description:
                        rows = cur.fetchall()
                        cols = [desc[0] for desc in cur.description]
                        df = pd.DataFrame(rows, columns=cols)
                        df.to_excel(writer, sheet_name=f"Q{i}", index=False)
                except Exception as e:
                    print(f"Error executing statement in Q{i}: {e}")
                    any_failed = True
                    
    cur.close()
    conn.close()
    
    if any_failed:
        print(f"Export completed with errors. Some queries failed.")
    else:
        print(f"Successfully exported all queries to {excel_path}")

if __name__ == '__main__':
    export_queries()
