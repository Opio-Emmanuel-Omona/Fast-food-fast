# Fast-food-fast
Fast-Food-Fast is a food delivery service app for a restaurant.

[![Build Status](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast.svg?branch=frontend)](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast)

[![Coverage Status](https://coveralls.io/repos/github/Opio-Emmanuel-Omona/Fast-food-fast/badge.svg?branch=frontend)](https://coveralls.io/github/Opio-Emmanuel-Omona/Fast-food-fast?branch=frontend)

[![Maintainability](https://api.codeclimate.com/v1/badges/72822b2801edfcc8895b/maintainability)](https://codeclimate.com/github/Opio-Emmanuel-Omona/Fast-food-fast/maintainability)


## Application URL
https://fast-food-fast-op.herokuapp.com/

# SETUP
## Requirements
    - Python installed
    - Any Text Editor

## Installation and setup
Run the following in your command line

    - pip install flask
    - pip install virtualenv
    - virtual venv
    - venv\Sripts\activate 
    - pip install Flask-RESTful

## Testing
The backend of the application can be tested using POSTMAN or the API documentation from this url
https://fast-food-fast-op.herokuapp.com/apidocs/


## API endpoints for the application
Request|URL|Description
---|---|---
**POST**|`/auth/signup`|Register User
**DELETE**|`/auth/login`|Login User
**GET**|`/orders`|Get all orders
**GET**|`/orders/orderId`|Fetch a specific order by its ID
**POST**|`/users/orders`|Place new order
**GET**|`/users/orders`|Order history
**PUT**|`/orders/orderId`|Update order status
**GET**|`/menu`|Get available menu
**POST**|`/menu`|Add a meal