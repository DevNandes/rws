import pymysql.cursors
from os import environ
from libs.tools import handle

def get(query, parameters = ""):
  connection = get_connection()
  payload = cursor_execute(connection, query, parameters)
  return payload


def insert(query, parameters):
  connection = get_connection()
  payload = cursor_execute(connection, query, parameters)
  return payload


def update(query, parameters):
  connection = get_connection()
  payload = cursor_execute(connection, query, parameters)
  return payload


def delete(query, parameters):
  connection = get_connection()
  payload = cursor_execute(connection, query, parameters)
  return payload


def cursor_execute(connection, query, parameters):
  with connection.cursor() as cursor:
    try:
      if (parameters):
        cursor.execute(query, (parameters))
      else:
        cursor.execute(query)
      connection.commit()
    except Exception as error:
      cursor.close()
      connection.close()
      handle.error(f"Failed to execute the query: {error}", 500)

    try:
      result = cursor.fetchall()
    except Exception as error:
      cursor.close()
      connection.close()
      handle.error(f"Failed to fetch result", 500)

    if (not (result)):
      payload = {
        "code": 204,
        "affected": cursor.rowcount,
        "insert_id": cursor.lastrowid,
        "data": 0
      }
    else:
      payload = {
        "code": 200,
        "data": result,
        "affected": cursor.rowcount,
        "insert_id": cursor.lastrowid
      }

    try: 
      cursor.close()
    except Exception as error:
      connection.close()
      handle.error(f"Failed to close cursor", 500)

    try: 
      connection.close()
    except Exception as error:
      handle.error(f"Failed to close connection", 500)

    return payload


def get_connection():
  try:
    connection = pymysql.connect(host=environ["MYSQL_HOST"], user=environ["MYSQL_USER"], database=None, password=environ["MYSQL_PASSWORD"], port=int(environ["MYSQL_PORT"]), cursorclass=pymysql.cursors.DictCursor, charset="utf8mb4", use_unicode=True)
  except Exception as error:
    handle.error(f"Failed to establish connection to the database server: {error}", 500)
  return connection
