import configparser
import psycopg2

class ConnectionDB:
  """ Make connection to database """
  config = configparser.ConfigParser()
  config.read('confi.ini')
  #Connect to PSQL
  try:
    connection = psycopg2.connect(user=config['postgresql']['user'],
                  password=config['postgresql']['password'],
                  host=config['postgresql']['host'],
                  port=config['postgresql']['port'],
                  database=config['postgresql']['database'])
    cursor = connection.cursor()
  except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
  finally:
    # closing database connection.
    if connection:
      print("PostgreSQL connection is active")
      #print(cursor)
      #print(connection)
      #cursor.close()
      #connection.close()
      #print("PostgreSQL connection is closed")

if __name__ == '__main__':
    ConnectionDB()