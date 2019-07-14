from airflow.utils.db import provide_session
from airflow.models import Connection


@provide_session
def get_conn(conn_id, session=None):
    conn = session.query(Connection).filter(Connection.conn_id == conn_id).first()
    return conn
