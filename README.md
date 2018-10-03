# Fast-food-fast
Fast-Food-Fast is a food delivery service app for a restaurant. (V2) Using Persistant data

[![Build Status](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast.svg?branch=api_v2)](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast)

[![Coverage Status](https://coveralls.io/repos/github/Opio-Emmanuel-Omona/Fast-food-fast/badge.svg?branch=api_v2)](https://coveralls.io/github/Opio-Emmanuel-Omona/Fast-food-fast?branch=api_v2)

[![Maintainability](https://api.codeclimate.com/v1/badges/72822b2801edfcc8895b/maintainability)](https://codeclimate.com/github/Opio-Emmanuel-Omona/Fast-food-fast/maintainability)


Different Endpoints have been created for the user and admin. The table below shows the different endpoints and methods used to access them. Append the endpoint to the base URL of the application to access them. So in a chronological order.


    1.      '/api/v2/auth/signup'       method = POST            Register a new user

This will create an account for the user. The data in the POST should be json data and the keys should be  

                {
                    'username': '',
                    'password': '',
                    'email': '',
                    'phone_no': ''
                }

Note that all the values are stringd and none of the values is null


    2.      '/api/v2/auth/login'         method = POST           Loggin in

This will sign in the user and return a token. The token should be copied. The data to post should be

                {
                    'username': '',
                    'password': ''
                }

The username and password should be the same as the one used to sign up

   
    3.      '/api/v2/menu'               method = GET            User only access

This is used by the user to view the menu. If using POSTMAN ensure to add the token to the Authorization > Token Bearer field. This will show the user the available menu


    4.      '/api/v2/users/orders'      method = POST           User only access

This will place allow the user to place an order for food based on the items from the database. Again don't forget the token. The data should be in the model below

            {
                "item_name": ''
            }


    5.      '/api/v2/users/orders'      method = GET            User only access

This will enable the user view the history of the orders that they made. Don't forget the token.


    6.      '/api/v2/menu'              method = POST           Admin only

The admin can add a meal option to the menu. Ensure to login as an admin and use admin token


    7.      '/api/v2/orders'            method = GET            Admin only

The admin can view all the orders that have been placed. Use admin token


    8.      '/api/v2/orders/order_id'   method = GET            Admin only

The admin can fetch a specific order


    9.      '/api/v2/orders/order_id'   method = PUT            Admin only

The admin can update an order status. Use admin token and data should be in the form below

                {
                    'status_name': option
                }

the option can be ['New', 'Processing', 'Cancelled', 'Complete']