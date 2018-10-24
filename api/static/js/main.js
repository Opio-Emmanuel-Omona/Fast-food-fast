function signup(e) {
    e.preventDefault();

    var user_detail = JSON.stringify({
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        phone_no: document.getElementById('phone_no').value,
        password: document.getElementById('password').value
    });

    url = 'http://127.0.0.1:5000/api/v2/auth/signup';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: user_detail
    })
        .then((response) => response.json())
        .then(function (data) {

            if (data.status) {
                //successful => login
                url = 'HTTP://127.0.0.1:5000/home';
                window.location.href = url;
            } else {
                //display message to the user
                document.getElementById('error').innerHTML = data.message;
                url = 'HTTP://127.0.0.1:5000/#formElement';
                window.location.href = url;
            }

        });
}

function signin(e) {
    e.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    var user_detail = JSON.stringify({
        username: username,
        password: password
    });

    url = 'http://127.0.0.1:5000/api/v2/auth/login';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: user_detail
    })
        .then((response) => response.json())
        .then(function (data) {
            // display message to the user
            console.log(data);

            if (data.username == 'admin') {
                // admin user
                localStorage.setItem('token', data.token);
                url = 'HTTP://127.0.0.1:5000/admin';
                window.location.href = url;
            }
            else if (data.username != null) {
                // other users
                localStorage.setItem('token', data.token);
                url = 'HTTP://127.0.0.1:5000/home';
                window.location.href = url;
            }
            else {
                // display message to the user
                document.getElementById('error').innerHTML = data.message;
                url = 'HTTP://127.0.0.1:5000/login#formElement';
                window.location.href = url;
            }

        });
}

function getMenu() {
    // get the menu and display it
    url = 'http://127.0.0.1:5000/api/v2/menu';

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-type': 'application/json',
            'Authorization': localStorage.getItem('token')
        },
    })
        .then((response) => response.json())
        .then(function (data) {
            //display menu to the user
            var output = '';
            if (data['menu']) {
                for (let index = 0; index < data['menu'].length; index++) {
                    output += `
                        <div class="content-section-b">
                            <div class="content-area wh-100">
                                <img src="static/images/${data['menu'][index].item_name}.jpg" alt="Food image" width="100%" height="100%"/>
                            </div>

                            <div id="item_no${+index}" class="content-area w-100-h-60">
                                ${data['menu'][index].item_name}<br>
                                UGX ${data['menu'][index].price}<br>
                                <div class="inline">
                                <input id="${data['menu'][index].item_name}" type="number" value="1"/><br>
                                </div>
                            </div>

                            <div class="content-area w-50-h-100">
                                <button class="order-btn" onclick="placeOrder('${data['menu'][index].item_name}')">Order<button>
                            </div>
                        </div>
                    `;
                    console.log(data['menu'][index].item_name);
                }
            } else {
                output = `<p class="error">Please log in to view the menu</p>`;
            }

            document.getElementById('food_items').innerHTML = output;
        });
}

function orderHistory() {
    // get the order history and display
    url = 'http://127.0.0.1:5000/api/v2/users/orders';

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-type': 'application/json',
            'Authorization': localStorage.getItem('token')
        },
    })
        .then((response) => response.json())
        .then(function (data) {
            //display history to the user
            var output = '';
            if (data['history']) {
                if (data['history'].length == 0) {
                    output = `<p class="error">No history available</p>`;
                }

                for (let index = 0; index < data['history'].length; index++) {
                    output += `
                    <div class="content-section d-il-b" style="height:50px;  width: 55%;">
                        Item: ${data['history'][index].item_name}<br>
                        Status: ${data['history'][index].status_name}<br>
                        Quantity: ${data['history'][index].quantity}<br>
                    </div>
                    `;
                }

            }
            else {
                output = `<p class="error">Please log in to view the history</p>`;
            }

            document.getElementById('order_history').innerHTML = output;

        });
}

function placeOrder(item_name) {
    url = 'http://127.0.0.1:5000/api/v2/users/orders';

    var order_detail = JSON.stringify({
        item_name: item_name,
        quantity: document.getElementById(item_name).value
    });

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Authorization': localStorage.getItem('token')
        },
        body: order_detail,
    })
        .then((response) => response.json())
        .then(function (data) {
            // display message to the user
            console.log(data);

            if (data.status) {
                // order has been placed
                document.getElementById('orderStatusP').innerHTML = 'Order has been placed';
                document.getElementById('orderStatusF').innerHTML = '';
            }
            else {
                // failed to place order
                document.getElementById('orderStatusF').innerHTML = `${data.message}`;
                document.getElementById('orderStatusP').innerHTML = '';
            }
        });

    orderHistory();
}