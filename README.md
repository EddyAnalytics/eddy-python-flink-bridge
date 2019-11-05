# Eddy Python Flink Bridge

## Example Query
`INSERT INTO mySink SELECT payload.after.first_name, payload.after.id from customers`

## Example Definition Object
```
{
     "parallelism": 2,
     "query": "INSERT INTO BLA SELECT A FROM X",
     "schemas": {
         "mysql1.inventory.customers": {
             "type": "source",
             "schema": {
                 "payload": "ROW<>"
             }
         },
         "mysql1.inventory.orders": {
             "type": "source",
             "schema": {
                 "payload": "ROW<>"
             }
         }
         "sql_results": {
             "type": "sink",
             "schema": {
                 "payload": "ROW<>"
             }
         }
     }
 }
 ```
