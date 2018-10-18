//listen for the click of the submit-signup button
// document.getElementById('submit-signup').addEventListener('click', addUserAPI);

function signup(e) {
    e.preventDefault();
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let phone_no = document.getElementById('phone_no').value;
    let password = document.getElementById('password').value;

    var user_detail = JSON.stringify({
        username: username,
        email: email,
        phone_no: phone_no,
        password: password
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
            //display message to the user
            console.log(data);
            alert(data);
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
            //display message to the user
            alert(data);

            localStorage.setItem('token', data.token)

            //then redirect with the token to the home page
            url = 'HTTP://127.0.0.1:5000/home'
            window.location.href = url;
        });
}


function getOrders() {
    // get all the orderes and display them
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
            console.log(data);

            let output = '';
            for (let index = 0; index < data['menu'].length; index++) {
                output += `
                    <div class="content-section-b">
                        <div class="content-area wh-100">
                            <img src="images/chips-chicken.jpg" alt="" width="100%" height="100%"></img>
                        </div>

                        <div class="content-area w-50-h-100">
                            ${data['menu'][index].item_name}<br>UGX ${data['menu'][index].price}
                        </div>

                        <div class="content-area w-50-h-100">
                            <button class="order-btn">Order<button>
                        </div>
                    </div>
                `;
            }
            document.getElementById('food_items').innerHTML = output;
        });
}