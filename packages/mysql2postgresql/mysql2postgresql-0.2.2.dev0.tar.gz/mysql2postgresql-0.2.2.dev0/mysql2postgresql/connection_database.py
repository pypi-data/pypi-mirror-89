cython: bool
try:
    from mysql2postgresql_cython import mysql2postgresql as runner
    cython = True
except ImportError as e:
    import mysql.connector
    import psycopg2
    import psycopg2.extras
    cython = False


class mysql2postgresql:
    def __init__(self):
        self.db = None
        self.dbx = None
        self.DB = None
        self.DBX = None
        self.tables:list = []
        self.database:str = None
        self.limit:int = 10000
        self.connect_mysql_kwargs:dict = {}
        self.connectpostgresql_kwargs:dict = {}
    
    if cython:
        def connect_mysql(self, **kwargs):
            self.connect_mysql_kwargs = kwargs
    else:
        def connect_mysql(self, **kwargs):
            print('connecting mysql server ...')
            self.db = mysql.connector.connect(**kwargs)
            self.dbx = self.db.cursor()
            self.database = kwargs['db']
        
    def close_mysql(self):
        if self.db or self.dbx:
            print('close connect mysql ...')
            self.dbx.close()
            self.db.close()
    
    if cython:  
        def connect_postgresql(self, **kwargs):
            self.connectpostgresql_kwargs = kwargs
    else:
        def connect_postgresql(self, **kwargs):
            print('connecting postgresql server ...')
            self.DB = psycopg2.connect(**kwargs)
            self.DB.autocommit = True
            self.DBX = self.DB.cursor() 
            self.DBX.execute("set client_encoding = 'utf8'")
        
        
    def close_postgresql(self):
        if self.DB or self.DBX:
            print('close connect postgresql ...')
            self.DBX.close()
            self.DB.close()
    
    
    #-------------------------------------------------------------------#
    def setval(self, table:str, serial_name:str):
        '''
            function setval to sequnce (seq) in PostgreSQL from Last ID
            Setdefault value for sequence when insert new data
        '''

        psql:str = f"SELECT {serial_name} FROM {table} ORDER BY {serial_name} DESC LIMIT 1"
        print(psql)
        self.DBX.execute(psql)
        id:int = self.DBX.fetchone()[0]
        psql = f"SELECT SETVAL('{table[0:56]}_{serial_name}_seq', {id})"
        self.DBX.execute(psql)
        # self.DB.commit()
                
                
    def insertinto(self, rows:list, table:str) -> None:
        '''
            Function insert data to PostgreSQL from function selecttoinsert 
        '''
        
        psql:str = f"INSERT INTO {table} values %s"
        print(psql)
        psycopg2.extras.execute_values(self.DBX, psql, rows)
        # self.DB.commit()
        
    #-------------------------------- function select mysql ---------------------------------------#
    def selecttoinsert(self, table:str) -> None:
        '''
            Function Select data from MySQL to function insertinto 
        '''
        
        step:int = 0 
        msql_arr:list = []
        rows:list = []
        msql:str = f'SELECT COUNT(*) FROM {table}'
        self.dbx.execute(msql)
        count:int = self.dbx.fetchone()[0]
        
        while count > 0:
            msql_arr.append(f'SELECT * from {table} LIMIT {self.limit} OFFSET {step};')
            step = step + self.limit
            count = count - self.limit
            
        for msql in msql_arr:
            print(msql)
            
            self.dbx.execute(msql)
            rows.extend(iter(self.dbx.fetchall()))
    
        self.insertinto(rows, table)
            

    def create_sequence(self, table:str, name:str):
        '''
            function create sequnce (seq) in PostgreSQL
            create sequence by tablename_primarykey_seq
        '''

        psql:str = f"DROP SEQUENCE {table[0:56]}_{name}_seq CASCADE"
        try:
            self.DBX.execute(psql)
        except:
            pass
        # self.DB.commit()
            
        psql = f"CREATE SEQUENCE {table[0:56]}_{name}_seq"
        self.DBX.execute(psql)
        # self.DB.commit()


    def main(self) -> None:
       
        ''' show column from MySQL to create table in PostgreSQL '''
        
        if len(self.tables) == 0:
            mysql= f'show tables from {self.database}'
            self.dbx.execute(mysql)
            tables:generator = (table_name[0] for table_name in iter(self.dbx.fetchall()))
        else:
            tables:generator = iter(self.tables)
        
        for table in tables:
            
            primary:list = []
            serial_names:str = ''
            primary_key:str = ''
            
            drop_psql:str = f'DROP TABLE IF EXISTS {table}'
            try:
                self.DBX.execute(drop_psql)
            except Exception as e:
                print(e)

        
            mysql:str = f'SHOW COLUMNS FROM {table}'
            self.dbx.execute(mysql)

            '''
            create table in PostgreSQL
            '''
            
            psql:str = f'CREATE TABLE IF NOT EXISTS {table} ('

            for row in iter(self.dbx.fetchall()):
                
                name:str=row[0]; typed:str=row[1]; null:str=row[2]; key:str=row[3]; default:str=row[4]; extra:str=row[5]
                
                '''
                    this change data type from MySQL to PostgreSQL
                '''
                if 'int' in typed: typed='int'
                elif 'tinyint' in typed: typed='int4'
                elif 'bigint' in typed: typed='int8'
                elif 'blob' in typed: typed='bytea'
                elif 'datetime' in typed: typed='timestamp without time zone'
                elif 'date' in typed: typed='date'
                elif 'text' in typed: typed='text'
                elif 'varchar' in typed: typed='character varying'
                elif 'double' in typed: typed='double precision'
                elif 'enum' in typed: typed='character varying'     
                    
                if key == 'PRI':
                    ''' when column is primary it append to list'''
                    primary.append(name)

                if extra == "auto_increment":
                    ''' when column is auto_increment'''

                    serial_names = name
                    self.create_sequence(table, name)
                    default = f"DEFAULT nextval('{table[0:56]}_{name}_seq'::regclass)"
                    psql+= f'{name} {typed} {default},'
                    
                else:
                    ''' when column is not auto_increment'''
                    if default is not None:
                        default = default.strip("()")
                        if typed == 'date' :
                            default = f"DEFAULT DATE('{default}')"
                        elif typed == 'timestamp' or default == 'NULL' or default.startswith("'"):
                            default = f'DEFAULT {default}'
                        else:
                            default = f"DEFAULT '{default}'"
                        psql+= f'{name} {typed} {default},'
                    else:
                        psql+= f'{name} {typed},'

            if len(primary) != 0:
                primary_key = ', '.join(primary)

            if primary_key != '':
                ''' add primary key from list '''
                psql+= f'PRIMARY KEY ({primary_key})'

            create_psql:str=psql.strip(',')+')'

            print(create_psql)
            
            self.DBX.execute(create_psql)
            # self.DB.commit()
            
            self.selecttoinsert(table)
            if len(serial_names) > 0:
                self.setval(table, serial_names)
            
    def run(self):
        if cython:
            print('Running in Cython version')
            try:
                runner.mysql2postgresql(self.connect_mysql_kwargs, self.connectpostgresql_kwargs, self.tables, self.limit)
            except Exception as e:
                print(e)
            finally:
                self.close_postgresql()
                self.close_mysql()
                
        else:
            print('Running in Python version')
            try:
                self.main()
            except Exception as e:
                print(e)
            finally:
                self.close_postgresql()
                self.close_mysql()
        