Run DBT commands

So far only the following IPython magics are implemented:

# Line magics
`%dbt rpc <args>`
it will run dbt rpc in the background. The args will be passed directly to dbt as command line arguments.

# Cell magics
`%%compile_sql`
the sql query in the cell will be compiled with the DBT RPC server and IPython will output the text

`%%run_sql`
the sql query in the cell will be run on the DBT RPC server and IPython will output the agate table. Also, it will run its `.print_table()` method
