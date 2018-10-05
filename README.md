# Fast-food-fast
Fast-Food-Fast is a food delivery service app for a restaurant. (V2) Using Persistant data

[![Build Status](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast.svg?branch=feedback)](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast)

[![Coverage Status](https://coveralls.io/repos/github/Opio-Emmanuel-Omona/Fast-food-fast/badge.svg?branch=feedback)](https://coveralls.io/github/Opio-Emmanuel-Omona/Fast-food-fast?branch=feedback)

[![Maintainability](https://api.codeclimate.com/v1/badges/72822b2801edfcc8895b/maintainability)](https://codeclimate.com/github/Opio-Emmanuel-Omona/Fast-food-fast/maintainability)


## Application URL
https://fast-food-fast-eomona.herokuapp.com/

# SETUP
## Requirements
    - Python
    - Any Text Editor
    - Pytest

## Installation and setup
Run the following in your command line

    - pip install flask
    - pip install virtualenv
    - virtual venv
    - venv\Sripts\activate 
    - pip install Flask-RESTful

## Testing
From the API documentation at the application url


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