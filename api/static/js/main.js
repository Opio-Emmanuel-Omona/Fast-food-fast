//listen for the click of the submit-signup button
// document.getElementById('submit-signup').addEventListener('click', addUserAPI);

function signup(event) {
    event.preventDefault();
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

function signin() {

}