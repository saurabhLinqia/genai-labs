import psycopg2
from pgvector.psycopg2 import register_vector


class PgClient():
    
    def __init__(self, dbcreds=None):
        # set dbcreds object
        self.dbcreds = dbcreds

    # def get_secret_as_json(self, secretid):
    #     # Create a Secrets Manager client
    #     get_secret_value_response = secrets_client.get_secret_value( SecretId=secretid )
    #     return json.loads(get_secret_value_response['SecretString'])

    def connect(self, dbname = "postgres", register_vector=False):
        dbhost = self.dbcreds['host']
        dbport = self.dbcreds['port']
        dbuser = self.dbcreds['username']
        dbpass = self.dbcreds['password']
        # dbname = "awsdocs"
        print(f'connecting to {dbname} on {dbhost}:{dbport}...')
        self.dbconn = psycopg2.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname, port=dbport, connect_timeout=10)
        self.dbconn.set_session(autocommit=True)
        print("connection established")
        self.dbcur = self.dbconn.cursor()
        if register_vector:
            self.register_vector()

    def register_vector(self):
        register_vector(self.dbconn)

    def execute(self, sql, vals=None):
        if not vals:
            return self.dbcur.execute(sql) 
        else:
            return self.dbcur.execute(sql,vals)
    
    def query(self, sql, vals=None):
        self.execute(sql, vals)
        return self.dbcur.fetchall()

    def close(self):
        print('closing cursor and connection')
        self.dbcur.close()
        self.dbconn.close()
        print("connection closed.")



