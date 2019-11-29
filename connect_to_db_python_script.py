import pymysql # This is a library allowing us to interact with mysql databases using Python

# These are the key variables needed to access you database.
# You can find them on the AWS RDS page when you click the link to your
# database instance. 

database_instance_endpoint=<yourDatabaseInstanceEndpointAsString>
port=3306 # Default port for mysql.
dbname="mydb"
user=<yourDatabaseUserAsString> # This is the database instance user you defined while creating your database
password=<yourDatabseUserPasswordAsString> # This is the database instance user's password

# Here we create a connection object 'con'
con = pymysql.connect(database_instance_endpoint, user=user,port=port,
                      passwd=password,database =dbname)

# Create a cursor using your connection, and use your cursor to query you db
cur = con.cursor()

# This sql query creates a `users` table with some fields
create_table_qry="""CREATE TABLE IF NOT EXISTS `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;"""

# The execute method of a cursor will execute SQL commands
cur.execute(create_table_qry) 

# However, until you commit the changes in your cursor, it's not reflected in your AWS database
cur.execute(create_table_qry)       

# But the users table is empty if it's just been created. So let's add a user:
sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"

# This format looks a bit strange but it's a secure way to insert data into a database.
# This format of inserting secures against something called SQL injection. Google it for more details - it's very clever engineering!
cur.execute(sql, ('testingtesting@boing.org', 'so-super-secret'))             

# And commit the changes
con.commit()

# And finally, let's double check that our insert query worked by performing a SELECT query
cur.execute("SELECT * FROM users")
cur.fetchall()

# And voila. You have sucessfully connected to your database, created < table, inserted into it and then retrieved from it. All from a remote Python interpreter.
