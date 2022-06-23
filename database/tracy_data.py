import pyodbc # module that accesses ODBC (MySQL) databases

details = {                     # information to access server
    "user": "ute_limited",
    "password": "VB6PlU$WcbDBqZ3m0IDX",
    "server": "timemachine1sql.berea.edu",
    "db": "UTE"
}

# uniform resource identifier contains name which refers to an object in the web
pyodbc_uri = 'DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['server'],details['db'],details['user'],details['password'])

pyconn = pyodbc.connect(pyodbc_uri)  # connects a tcp based client socket to a tcp based server socket
c = pyconn.cursor()  # allows python to execute sql database command??
for row in c.execute('select * from STUPOSN'):
    print("PYODBC:",row)
    break
