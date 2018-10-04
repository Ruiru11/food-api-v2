# FAST-FOOD-FAST API-V2
> An api service for the fast-food-fast project
> Used to manage requests for the project





## Clonning the repo

OS X, Linux & Windows::

```sh
git clone https://github.com/Ruiru11/food-api-v2.git
```



## Installing dependecies 



```sh
pip install -r requirements.txt
```

## Release History

* v1.0
    * CHANGE: integrate a database
    * Implement authentication 



# Endpoints: 
## user-signup(POST) :
- route: http://127.0.0.1:5000/api/v2/signup
- data is enetred in json format{ "username","password","email","address"}
 ## user-signin(POST):
- route:http://127.0.0.1:5000/api/v2/signin
- data is eneterd in json format{ "email","password"}
 ## creating an order(POST):
- route:http://127.0.0.1:5000/api/v2/orders
- data is eneterd in json format{"item","cost","description"}
 ## getting all orders(GET):
- route:http://127.0.0.1:5000/api/v2/orders
 ## getting a specific order using its id(GET):
- route:http://127.0.0.1:5000/api/v2/orders/id
 ## deleting an oder(use its specific id)(DELETE):
- route:http://127.0.0.1:5000/api/v2/orders/id
 ## updating an order(use its specific id)(PUT):
- route:http://127.0.0.1:5000/api/v2/orders/id
- status is changed from starting to delivered
- input is in json format{"status" "deliverd"}

* use the given endpoints, data should be from postman  



# Running the api
- on your terminal:
 
 1. git clone https://github.com/Ruiru11/food-api-v2.git
 2. cd into food-api-v2
 3. activate virtualenv
 3. pip install -r requirements.txt
 4. run python run.py run
 5. make sure to have a postgress database 

