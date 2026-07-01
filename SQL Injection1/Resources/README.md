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

The page accests an 