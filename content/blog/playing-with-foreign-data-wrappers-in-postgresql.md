---
author: Gavin Fleming
date: '2014-08-16'
description: Recently I set out to try out the PostgreSQL foreign data wrapper (FDW).
erpnext_id: /blog/database/playing-with-foreign-data-wrappers-in-postgresql
erpnext_modified: '2014-08-16'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Database
thumbnail: /img/blog/placeholder.png
title: Playing with Foreign Data Wrappers in PostgreSQL
---

Recently I set out to try out the PostgreSQL [foreign data wrapper ](<https://wiki.postgresql.org/wiki/Foreign_data_wrappers>)(FDW) because I needed access to data that was in MySQL tables. The main reason I needed to play around was to expose my data to a range of PostgreSQL functions that are better and more recent that MySQL. I also needed to use MySQL data for views and lookups and data-driven styling for some Geoserver layers. FDWs allow remote access to tables or queries from various external third-party databases or file structures.

So this is a workflow I followed to do this on Ubuntu 14.04:

Install PostgreSQL and MySQL development files :  


>   
> 
>     
>     
>     sudo apt-get install libpq-dev  postgresql-server-dev-9.3  
>     > sudo apt-get install libmysqlclient-dev
> 
>   
> 

  
Clone mysql_fdw in your development folder:  


>   
> 
>     
>     
>     git clone [git@github.com:EnterpriseDB/mysql_fdw.git](<mailto:git@github.com:EnterpriseDB/mysql_fdw.git>)
> 
>   
> 

  
CD into the mysq_fdw folder and run the following:  


>   
> 
>     
>     
>     export PATH=_/ usr/lib/postgresql/9.3/bin/_:/usr/bin/mysql:$PATH make USE_PGXS=1  
>     > sudo PATH=_/ usr/lib/postgresql/9.3/bin/_:/usr/bin/mysql:$PATH make USE_PGXS=1 install
> 
>   
> 

  
Then the SQL begins in PostgreSQL database by creating a database on the terminal or using your favourite gui (pgadmin3).  
Create a database where you will have all your tables:  


>   
> 
>     
>     
>     createdb mysql_fdw  
>     > psql -c 'CREATE EXTENSION postgis;' mysql_fdw  
>     > 
> 
>   
> 

  
or in pgadmin create a database and then log into the database then run the following command:  


>   
> 
>     
>     
>     CREATE EXTENSION mysql_fdw;
> 
>   
> 

  
create a server that points to a database that you need remote access to:  


>   
> 
>     
>     
>     CREATE SERVER mysql_svr   
>     > FOREIGN DATA WRAPPER mysql_fdw   
>     > OPTIONS (address '127.0.0.1', port '3306');
> 
>   
> 

  
create a corresponding table to hold the data in PostgreSQL as a foreign table by selecting the values from mysql database "test":  


>   
> 
>     
>     
>     CREATE FOREIGN TABLE local_cadastre (  
>     > sg21 character varying (255),  
>     > province character varying (255),  
>     > munname character varying (255)  
>     > )  
>     > SERVER mysql_svr  
>     > OPTIONS (query 'SELECT sg21,province munmane from test.cadastre limit 500;');
> 
>   
> 

  
Create user connection parameters in your database where you define the connection parameters to the mysql database:  


>   
> 
>     
>     
>     CREATE USER MAPPING FOR PUBLIC   
>     > SERVER mysql_svr   
>     > OPTIONS (username 'user', password 'password123');
> 
>   
> 

  
After that you have your foreign table in PostgreSQL database and you could run a select statement to return records from the table you have created. The data is dynamically fetched from MySQL tables and viewed in PostgreSQL.

If the data you are fetching from MySQL is static you can run the following to create a local copy of the table:  


>   
> 
>     
>     
>     Create table  cadastre as select * from local_cadastre;
> 
>   
> 

  
After that you have a PostgreSQL table and we can do our favourite PostgreSQL functions on our data. An advantage is if you had data in other databases and you have moved from them to our favourite PostgreSQL, but you need to keep the other database going for legacy clients, then don't worry about moving the data just maintain it where it is and play around with foreign data wrappers.
