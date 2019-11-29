import pymysql # This is a library allowing us to interact with mysql databases using Python

# These are the key variables needed to access you database.
# You can find them on the AWS RDS page when you click the link to your
# database instance. 

database_instance_endpoint=<yourDatabaseInstanceEndpointAsString>
port=3306 # Default port for mysql.
dbname=<youDatabaseName> # Not your database-instance-name, you database name. In the tutorial, we alled it 'mydb' 
user=<yourDatabaseUserAsString> # This is the database instance user you defined while creating your database
password=<yourDatabseUserPasswordAsString> # This is the database instance user's password

# Here we create a connection object 'con'
con = pymysql.connect(database_instance_endpoint,
                      user = user,
                      port = port,
                      passwd = password,
                      database = dbname)

# Create a 'cursor' using your connection. You use a cursor to query your db
cur = con.cursor()

# This sql query creates a `users` table with email, password and id fields
create_table_qry="""CREATE TABLE IF NOT EXISTS `users` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `email` varchar(255) COLLATE utf8_bin NOT NULL,
                    `password` varchar(255) COLLATE utf8_bin NOT NULL,
                     PRIMARY KEY (`id`)
                     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                     AUTO_INCREMENT=1 ;"""

# The execute method of the cursor will execute SQL commands
cur.execute(create_table_qry) 

# However, until you call the 'commit' method on your connection object, the AWS database is not syncronised with your changes
cur.execute(create_table_qry)       

# Well done! Now you have a users table! But it's empty...
# So let's add a user
# The following SQL insert query format may look a bit strange but it's a secure way to insert data into a database.
sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
cur.execute(sql, ('testingtesting@boing.org', 'so-super-secret'))  
# This format of inserting secures against something called 'SQL injection'. Google it for more details - it's very clever engineering!
           
# The insert has been made but we haven't committed the changes yet. So let's do it:
con.commit()

# And finally, let's double check that our insert query worked by performing a SELECT query
cur.execute("SELECT * FROM users")

# When you use a SELECT query to retrieve data from a database, they are stored within your cursor object.
# You can retrive them one at a time, all at once or in specific quantities. As we only have a small numebr of records, we can can go ahead and 'fetchall' of them:
cur.fetchall()

# And voila! If you can see user dat appear in your PYthon interpreter, you have sucessfully connected to your database, created a table, inserted into it and then retrieved from it. All from a remote Python interpreter.
