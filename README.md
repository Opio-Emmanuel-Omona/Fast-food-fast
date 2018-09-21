# Fast-food-fast
Fast-Food-Fast is a food delivery service app for a restaurant.

[![Build Status](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast.svg?branch=api)](https://travis-ci.com/Opio-Emmanuel-Omona/Fast-food-fast)

[![Coverage Status](https://coveralls.io/repos/github/Opio-Emmanuel-Omona/Fast-food-fast/badge.svg?branch=api)](https://coveralls.io/github/Opio-Emmanuel-Omona/Fast-food-fast?branch=api)

The application User Interfaces can be accessed on the link below:
https://opio-emmanuel-omona.github.io/Fast-food-fast/UI/



1. The flow is from Signup.html where an account is created

2. After an account has been created, then one can log in form signin.html

3. The home page is where the user can make orders and also view history

4. The admin page is where the admin handles all the orders made by users. 


Note: There's no functionality yet, therefore one can access the various pages by
      the links in the navigation bar.

      To access the admin user interface, use the link below:
       https://opio-emmanuel-omona.github.io/Fast-food-fast/UI/admin.html

      Also most of the data is static and will be later changed

link to pivaotal tracker:
https://www.pivotaltracker.com/n/projects/2195460


link to github account:
https://github.com/Opio-Emmanuel-Omona/Fast-food-fast


API

The API endpoints can be tested using the postman chrome extension.

The url to submit in postman is given below:

https://fast-food-fast-eomona.herokuapp.com

Diferent endpoints were used and the work flow for testing is given below:

            
      1. /api/v1/orders                method = GET               returns all the orders placed
      2. /api/v1/orders                method = POST              for placing a new order
      3. /api/v1/orders/<id>           method = GET               returns a specifig order at the given id
      4. /api/v1/orders/<id>           method = PUT               to update an order at the given id
      5. /api/v1/orders/<id>           method = DELETE            to delete an order at the specified id


Note: 1. When using postman append the end points to the url

      2. It is recommended to view the output in raw json/application

      3. Also when using POST or PUT methods in the body use raw/application and the format of a post should be
      {"id": "value-int", "username": "value-str", "item": "value"}
      The keys should be exact and identical to the ones used in this example.

      4. For the DELETE method, only an id is provided as shown below
      {"id": "1"}
      to delete the request with id =1. You can only delete a request that has been posted using POST 