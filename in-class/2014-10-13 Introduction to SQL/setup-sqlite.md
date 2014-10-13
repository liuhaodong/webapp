SQLite setup notes
====================

Follow these directions if you have not already installed Postgres and Psycopg2.  If you are a Linux or Mac user you might already have `sqlite3` installed on your laptop.  If you do not have `sqlite3` already installed (and cannot quickly install it), please clone your repository and follow these instructions on linux.andrew.cmu.edu instead.


## Creating the database schema

The sample application is configured to use Postgres, not SQLite, so you 
cannot simply use the Django tools to create the database schema and
populate the database. Instead, you can use the `setup.sql` file we
provided in the application directory:

+ `sqlite3 database.sdb < setup.sql`

Alternatively you may reconfigure the Django application to use SQLite
(in `settings.py`) and then use `makemigrations`, `migrate`, and `loaddata`
as described in the Postgres instructions.

## Access the shell:

You should then be able to use the SQLite shell:

+ `sqlite3 database.sdb` 

## Can't get Postgres or SQLite working?

If you cannot use either Postgres or SQLite in class, you might use an online
SQL interpreter such as http://www.compileonline.com/execute_sql_online.php.
You will need to load the `setup.sql` file there.  (We have not tested these
options.)

