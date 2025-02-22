"""
this code is to read the table created from rule component. The table goes:
 CREATE TABLE IF NOT EXISTS t_check_role_code (
        id SERIAL PRIMARY KEY,
        role_id INTEGER REFERENCES t_check_roles (id),
        code_block TEXT,
        create_time TIMESTAMP DEFAULT NOW(),
        enable BOOLEAN,
        start_time TIMESTAMP,
        end_time TIMESTAMP
    );
We traverse the entire table and execute the python code or lua code in code_block if the conditions are met. Repeat the traversal.
"""
import psycopg2

# 数据库连接参数
conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '7PIug1Lk3O',
    'host': 'pg-postgresql',
    'port': '5432',
    'sslmode': 'disable',
}

# 遍历搜索并执行代码块
def execute_code_blocks():
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    # 查询满足条件的记录
    select_query = '''
    SELECT code_block
    FROM t_check_role_code
    WHERE enable = TRUE AND start_time <= NOW() AND end_time >= NOW();
    '''
    cur.execute(select_query)
    rows = cur.fetchall()

    # 执行代码块
    for row in rows:
        code_block = row[0]
        try:
            exec(code_block)
        except Exception as e:
            print(f"Error executing code block: {str(e)}")

    cur.close()
    conn.close()

# 持续执行搜索和执行代码块的操作
while True:
    execute_code_blocks()