# Creating an AWS Relational Database Using RDS and conencting to it using Python 3.7

## Setting up the infrastructure
### In the following steps, we'll create the cloud space for your database to live.

1. **Create a VPC** for this tutorial called **Test_SQL_DB_VPC** at **10.0.0.0/16**. You'll need to double **check the DNS Hostnames and DNS Resolution from the actions button and make sure both are enabled.** This is to ensure that later, we can access from outside the VPC. 

![DNS VPC Settings](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/dns_vpc.png)

2. **Create an internet gateway** called **Test_SQL_DB_IGW** and attach it to *Test_SQL_DB_VPC*
3. When creating a relational database using the AWS RDS, **the VPC must have a minimum of 2 subnets in *different* availability zones**. The database will automtically exist as 2 continuously syncronised copies of each other, one in each subnet. One is called the 'master' db, and the other is called the 'slave' db. In case of a catastrophic error in one subnet, ***AWS will automatically make the surviving db the 'master' db and create a new 'slave' db to replace the lost one***. So go ahead and create 2 subnets, associated to Test_SQL_DB_VPC with the CIDR block **10.0.1.0/24** and **10.0.2.0/24**. ***It's vital that the subnets are not in the same availability zone!***

**Also, take a note of the names of the availability zones your subnets are in. You'll need them later**.

4. Create a new security group called **TEST_SQL_DB_SG** with an inbound rule of all traffic **from your ip**. This means that only your device can access it.

5. Select one of the newly created subnets. It doesn't matter which one because both of them will refer to the same route table. Enter that route table, press the edit button and **add a new line specifying that 0.0.0.0/0 traffic (anywhere outside of Test_SQL_DB_VPC) will be directed to our internet gateway**, Test_SQL_DB_IGW.
![User_Config](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/rt.png)
4. *It's important to control not just which IPs, ports and protocols attempt to access your database, but also which people and devices*. **The way to manage user permissions in AWS is with the IAM service**. You can create individual users with specific permissions, or user groups which have specific permissions which are inherited by any users within that group. Typical groups could be *admin, guest, applicationX* etc. For the purpose of this tutorial, we'll leave it at creating a sungle user, one with enough permissions to read and write to the future database. 

5. Search for the **IAM** service and follow the link. In the left hand panel you will see a **Users** link. Follow it and click the big blue **Create User** button.
6. In the user creation form, you must give your user a name and assign their permissions. In this tutorial, we can call the user **Test_SQL_DB_USER**. Ensure that programmatic access is given as well as AWS management console access.
![User_Config](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/1.png)
7. In the following screen, you can add Test_SQL_DB_USER to a group and set boundary permissions. This is essential in effectively managing a production level database - even for just a few users. Where there's someone in charge or someone less skilled, spend time on this. **For now in this tutorial, you can just copy the permissions from the existing user (you)**.
![User_Config](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/1_5.png)
8. In the next screen, you can add a 'Tag'. It's not necessary but very useful to identify from a table of complicated info exacfly what you're looking for. So let's add one:
![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/2.png)
9. On the next screen, review your user and assuming everything looks good, press the create user button. On the next screen you will see a summary of the user permissions, be able to **download a csv with all the imñortant user details including their access key ID and secret access id**. Store these details very securely on your local device. *You can optionally have an email sent with login instructions for the new user, though they wont include a password.*

## Creating the RDS database
1. Navigate via the services button to **RDS**. This interface may look a bit different than what you've seen so far but it's fairly simple to navigate. **Click the big orange 'Create Database" button.**
2. You'll be presented 2 options at the top of the page, 'easy create' and 'standard create'. *You may ask yourself why not make it easier? Well because most of the things it tries to simplify, you have already taken care of in previous steps of this tutorial. You've done everything exactly as you want it and you know exactly what kind of infrastructure you have. That said 'easy create' may not be a bad option for you in the future, just be careful about what kind of decisions are taken on your behalf. That said, **go ahead and select standard create MySQL.**
![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/3.png)
3. Scroll down the page. Select **free tier** and give your database instance the name **TestSQLDB**. There is an important difference to understand between what a database instance is, and what a database is.  Your database instance TestSQLDB can contain multiple databases, each unique and individual. This database instance is not an actual database but the host instance where you can create and manage the databases in your instance. Who will have access to all databases and the database instance itself? Usually an admin, which you should **assign a name and password here too.**

![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/4.png)

4. Make sure that the database is publicly available so we can later access it from another device:

![Public Access](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/db_public_access.png)

5. Assign the security group we created before, **TEST_SQL_DB_SG**.

6. As you selected the **free tier template**, most of the remaining options can be left as they are as there would have to be exended usage to incur any charges. One final configuration which is vital is to **designate the Test_SQL_DB_VPC as the VPC host of TestSQLDB**.

7. Remember you created a **database instance** before? ***In the additional configuration at the end of the form, you can create an actual database.***

![Public Access](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/6.png)

***Not understanding the difference between a database instance and a database on AWS will cause you many houses of head scratching.** Just know that in the create database process, you can create both at the same time.*

8. Go ahead and click the final orange "Create Database" button.

## Connecting to your database using the 'pymysql' library & Python3.7

You need to use Python for the next steps. **I am using using Python 3.7 but I'll just call it Python from here on in**. You should be using something later than 3.6 to ensure future proof code and void compatability issues with the code in this tutorial.

1. Open a command line interface of your choice. If you're not familiar with this term it may mean that you aren't aware that you have one. You do though, for sure. Windows users can search for Powershell or CMD (command prompt). Ubuntu or MACOS users can search for bash, shell or termial.

2. **Highly recommended but optional step **:

Create a Python environment for this tutorial. Get in to the habit of doing this to ensure you can always separate the one project's Python environment from another and that you can completely avoid dependency version issues. [Here's a good page for you to review related to this topic](https://realpython.com/python-virtual-environments-a-primer/)

3. OK so you're at the command line/terminal/powershell - whatever your chosen app is. You have created a Python environment for this tutorial and you've activated it. Now you need to install what you need for this part.

**pip install pymysql**

Once this is done, let's launch Python with the "Python" or "Python3" command (depending on system). If one doesn't work, try the other. 

4. OK so now you're on the Python interpreter. It looks like this:

![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/5_python.png)


If you want a much nicer python interpreter, install ***ipython***:

**pip install ipython**

..and call 'ipython' on the command line to start it. It looks like this:

![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/5_ipython.png)

Using ipython is optional but one of the beautiful things about ipython, is that **you can copy and paste multiple lines of code in to the ipython interpreter**.  

5. Take a look at the following python script. [The same script can be downloaded from this repository](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/connect_to_db_python_script.py)

```python
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
```
# And voila! If you can see user data appear in your Python interpreter, you have sucessfully connected to your database, created a table, inserted into it and then retrieved from it. All from a remote Python interpreter.




