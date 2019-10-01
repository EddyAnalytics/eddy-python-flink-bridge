INSERT INTO mySink SELECT payload.after.first_name, payload.after.id from customers
