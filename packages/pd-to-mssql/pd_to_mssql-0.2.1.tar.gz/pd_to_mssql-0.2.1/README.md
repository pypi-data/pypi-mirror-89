## pd_to_mssql : Quick upload of pandas dataframes to Microsoft SQL Server

---

### Value Proposition

The incredible functionality afford by [pandas](https://pandas.pydata.org/) can make automating [ETL tasks](https://en.wikipedia.org/wiki/Extract,_transform,_load) quick and painless, if that task does not involve uploading data to a Microsoft SQL Server, as the standard `to_sql` fucntion is [painfully slow](https://stackoverflow.com/questions/29706278/python-pandas-to-sql-with-sqlalchemy-how-to-speed-up-exporting-to-ms-sql). This package uses only pandas and [pyodbc](https://github.com/mkleehammer/pyodbc/) to achieve upload speeds comparable to [SSIS packages](https://docs.microsoft.com/en-us/sql/integration-services/integration-services-ssis-packages?view=sql-server-ver15) or [SQLAlchemy](https://www.sqlalchemy.org/) + pyodbc's `fast_executemany=True` option, while also keeping the existing table structure intact (i.e. dropping the target table and creating one with new column datatypes) and requiring only one line of code to do so.

### Possible Alternatives to pd_to_mssql

I attempted many other solutions to SQL Server upload before writing this package. Here is a brief list of those options and my main issue with them:

| Solution | Issue |
| --- | --- |
| Writing dataframes to csv and using the [bcp utility](https://docs.microsoft.com/en-us/sql/tools/bcp-utility?view=sql-server-ver15) | [bcp cannot handle the delimiting character appearing within a field value, even if it is properly quoted.](https://docs.microsoft.com/en-us/sql/relational-databases/import-export/specify-field-and-row-terminators-sql-server?view=sql-server-2017#characters-supported-as-terminators) Also, too much tedious work outside of python is required for each upload.
| Writing dataframes to excel and using SSIS packages launched by `subprocess.run()` and the [dtexec utility](https://docs.microsoft.com/en-us/sql/integration-services/packages/dtexec-utility?view=sql-server-ver15) | Works well, but requries a sql server instance to be installed in the deployment environment. Again, way too much tedious developement outside of python. |
| [pyodbc + SQLAchemy's `fast_executemany=True` option](https://stackoverflow.com/a/48861231/10992541) | Definitely the best of these options. Should work for most people. Not a fan of the behavior of the `if_exists='replace'` parameter, but workarounds are available. I ran into some memory issues while attempting to upload some expetionally large dataframes (1 million+ rows, 10+ columns), which prevented this from becoming my go-to solution (and no, I was not using the old "SQL Server" odbc driver). |

### How to install pd_to_mssql

`pip install pd_to_mssql`

### Dependencies

* [pandas](https://pandas.pydata.org/)
* [pyodbc](https://github.com/mkleehammer/pyodbc/)

### How to use pd_to_mssql
```python
from pd_to_mssql import to_sql
to_sql(df_in, table_name, cnxn_string, schema='dbo', index=True, replace=False, chunk_size=1000, thread_count=5, ignore_truncation=False, ignore_missing=False)
 ```
 
 | Parameter | Required/Default Value | Description |
 | --- | --- | --- |
 | df_in | Requried | Dataframe which will be uploaded to the SQL Server. |
 | table_name | Required | Upload destination. Specify only the table name. Do not include the schema. |
 | cnxn_string | Required | ODBC connection string. See [here](https://www.connectionstrings.com/microsoft-odbc-driver-17-for-sql-server/) for more information. |
 | schema | 'dbo' | Specify the target table's schema if need be. |
 | index | True | Upload the index to the target table. Will only be included if the index name matches a column in the target table. |
 | replace | False | Truncate the target table before uploading the data contained within df_in |
 | chunk_size | 1000 | Number of rows included in each insert statement. [1000](https://stackoverflow.com/questions/37471803/sql-server-maximum-rows-that-can-be-inserted-in-a-single-insert-statment) is the maximum number of rows allowed by MS SQL Server. |
 | thread_count | 5 | Number of concurrent connections established for insertion. Increasing this value will speed up perfomance as long as connection latency is the main bottleneck.|
 | ignore_truncation | False | Ignore string truncation when uploading string values with more characters than are allowed in the target column. This is accomplished by setting `ANSI_WARNINGS OFF`. |
 | ignore_missing | False | Instead of raising a `MissingColumnsException`, an attempt will be made to insert null values into that column instead. |

### How pd_to_mssql works
 
To start, all data contained within the dataframe is stringified to accomodate creation of the insert statements. Then a number of threads (from the threading module) are spawned in accordance with the `thread_count` parameter. Each of those threads then receives a separate pyodbc connection. A temporary table is created in each connection, and insertion into each temp table is conducted concurrently. Once temp table insertion is complete on all threads, the temp tables are unloaded one-by-one into the target table. This last step is only completed if all temp table insertions complete successfully.

### Column Mapping

For each non-identity column in the target table, a column with the same name must exist in the provided dataframe, but the data types of the those columns in the dataframe are irrelevant, as they will be cast to the correct data type based on the column specification. If the column does not exist in the provided dataframe, then a MissingColumnsException will be raised, unless `ignore_missing=True`, in which case null values will be inserted into the column, provided it is nullable.
 
 ### Debugging
 
 Some errors make it through the initial validation checks and are only caught once the insertion statement is generated. As such, the generated SQLExcetions generally contain very little useful information in identifying the issue. To assist in debugging, the first failing insert statement in each thread will be written to disk in a directory called `__pd_to_mssql_exception` located in the current working directory at the time of the upload. From there, you will be able to run those scripts in SSMS to easily identify where and why they are failing. In my experience, the most common issues which make it to this stage stem from invalid data conversions. E.G. unrecognized string representation of data formats (Convert to Datetime.Date(time) before upload) or string columns containing numeric data with a few instances of non-numeric characters.
 
 ### Miscellaneous Notes
 * Insertion will only be commited to the database if there are no errors. If there is a SQLException thrown, then no rows will be inserted into the target database.
 * If `replace=True` then table truncation will only occur if there are no errors during the temp table insertion process.
