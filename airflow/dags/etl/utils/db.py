# coding: utf-8
import os
import datetime
from sqlalchemy import create_engine

class PgConnector:
    def __init__(self):
        self.db_url = os.getenv("POSTGRES_URL")
        self.db_engine = create_engine(self.db_url, pool_pre_ping=True)

    async def get_query(self, to_table_name: str, data: dict):
        values = []
        for col in data.keys():
            if type(data[col]) in [str, datetime.datetime]:
                values.append("'{}'".format(data[col]))
            elif data[col] is None:
                values.append("null")
            else:
                values.append(str(data[col]))

        values_str = ", ".join(values)
        cols_str = ", ".join(data.keys())
        sql = """INSERT INTO {} ({}) VALUES ({})""".format(
            to_table_name, cols_str, values_str)
        return sql

    async def save_record(self, table_name: str, record: dict):
        conn = await asyncpg.connect(self.db_url)
        await conn.execute(await self.get_query(table_name, record))
        await conn.close()

    async def bulk_insert(self, table_name: str, cols: list, records: list):
        cols_str = ", ".join(cols)
        sql = """INSERT INTO {} ({}) VALUES ({})""".format(
            table_name, cols_str, ", ".join([f"${i+1}" for i in range(len(cols))]))
        conn = await asyncpg.connect(self.db_url)
        await conn.executemany(sql, records)
        await conn.close()

    def get_json_query(self, query):
        with self.db_engine.connect() as conn:
            result = conn.execute(query).first()

        return dict(result.items()) if result else {}

    def run_query(self, query):
        with self.db_engine.connect() as conn:
            conn.execute(query)
