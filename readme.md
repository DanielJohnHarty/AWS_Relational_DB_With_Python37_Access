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
2. You'll be presented 2 options at the top of the page, 'easy create' and 'standard create'. *You may ask yourself why not make it easier? Well because most of the things it tries to simplify, you have already taken care of in previous steps of this tutorial. You've done everything exactly as you want it and you know exactly what kind of infrastructure you have. That said 'easy create may not be a bad option, but you wont learn anything.* That said, **go ahead and select standard create MySQL.**
![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/3.png)
3. Scroll down the page. Select **free tier** and give your database the name **TestSQLDB**, and create a **user and password combo**.
![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/4.png)

4. Make sure that the database is publicly available so we can later access it from another device:

![Public Access](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/db_public_access.png)

5. Assign the security group we created before, **TEST_SQL_DB_SG**

4. As you selected the **free tier template**, most of the remaining options can be left as they are as there would have to be exended usage to incur any charges. One final configuration which is vital is to **designate the Test_SQL_DB_VPC as the VPC host of TestSQLDB**.

5. Finally, make sure that the check box allowing Go ahead and click the final orange "Create Database" button.

## Connecting to your database using the AWS 'Boto' library & Python3.7
### First things first, this is a tutorial. It is not documentation, it is not exhaustive and it is not 100% sure to be up to date in the future. Take the time to read the [Boto RDS Documentation](http://boto.cloudhackers.com/en/latest/rds_tut.html). It will open your eyes to the possibilities and act as a much better source of technical reference for you in the future.

1. You need to use Python for the next steps. I am using using Python 3.7 (I'll just call it Python from here on in). You should be using something later than 3.6 if you want to avoid problems.
2. **Highly recommended but optional step - ** create a Python environment for this tutorial. Get in to the habit of doing this to ensure you can always separate the one project's Python environment from another and that you can completely avoid dependency version issues. [Here's a good page for you to review related to this topic](https://realpython.com/python-virtual-environments-a-primer/)
3. OK so you're at the command line/terminal/powershell - whatever your chosen app is. You have created a Python environment for this tutorial and you've activated it. Now you need to install what you need for this part.

**pip install boto3**

Once this is done, let's launch Python with the "Python" or "Python3" command (depending on whether you're on Windows, Linux or Mac.

4. OK no you're on the Python interpreter. It looks like this:
![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/5_python.png)

If you want a much nicer python interpreter, install ipython:
**pip install ipython**
..and call 'ipython' on the command line to start it. It looks like this:
![User_Tag](https://github.com/DanielJohnHarty/AWS_Relational_DB_With_Python37_Access/blob/master/Images/5_ipython.png)

It's totally optional but I'm using ipython so don't worry if the images differ slightly from your own standard Python interpreter.

5. This is not a Python tutorial as such, so I will just give you a commented script which you can use to connect to your database:



