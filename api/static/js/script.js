function openpage(pageName, elmnt, color) {
	// Declare all variables
	var i, tabcontent, tablinks;

	// hide all the elements with class='tabcontent'
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}

	// give the tablinks a bankground color
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].style.backgroundColor = "#777";
	}

	document.getElementById(pageName).style.display = 'block';

	elmnt.style.backgroundColor = color;

	//call the method to fetch all the orders
	getOrders();
}

function allowDrop(ev) {
	ev.preventDefault();
}

function drag(ev) {
	ev.dataTransfer.setData("text/html", ev.target.id);
}

function drop(ev) {
	ev.preventDefault();
	var data = ev.dataTransfer.getData("text/html");
	ev.target.appendChild(document.getElementById(data));
}

function getOrders() {
	// get all the orders and display them according to status
	url = 'http://127.0.0.1:5000/api/v2/orders';

	fetch(url, {
		method: 'GET',
		headers: {
			'Content-type': 'application/json',
			'Authorization': localStorage.getItem('token')
		},
	})
		.then((response) => response.json())
		.then(function (data) {
			//display menu to the user only if ok
			console.log(data);

			// refresh the order status
			resetOrderStatusTabs();

			for (let index = 0; index < data['orders'].length; index++) {
				let output = `
					<div id="drag${+index}" draggable="true" ondragstart="drag(event)" class="content-section-b">
						${data['orders'][index].order_id}<br>
						${data['orders'][index].username}<br>
						${data['orders'][index].item_name}<br>
						${data['orders'][index].quantity}<br>
					</div>
				`;
				// Using contains because of the extra space in the status
				if (data['orders'][index].status.includes("New")) {
					document.getElementById('new_order').innerHTML += output;
				}
				else if (data['orders'][index].status.includes('Processing')) {
					document.getElementById('processing_order').innerHTML += output;
				}
				else if (data['orders'][index].status.includes('Cancelled')) {
					document.getElementById('cancelled_order').innerHTML += output;
				}
				else if (data['orders'][index].status.includes('Complete')) {
					document.getElementById('complete_order').innerHTML += output;
				}
				else {
					//error
				}
			}
		});
}

function addItem(e){
	e.preventDefault();

	url = 'http://127.0.0.1:5000/api/v2/menu';

	var menu_detail = JSON.stringify({
		item_name: document.getElementById('item_name').value,
		price: document.getElementById('price').value
	});

    fetch(url, {
        method: 'POST',
        headers: {
			'Content-type': 'application/json',
			'Authorization': localStorage.getItem('token')
        },
        body: menu_detail
    })
        .then((response) => response.json())
        .then(function (data) {
			console.log(data);
		});
}

function updateOrderStatus(orderId, newStatus){
	url = 'http://127.0.0.1:5000/api/v2/orders/'+orderId;

	var order_detail = JSON.stringify({
		status_name: newStatus
	});

    fetch(url, {
        method: 'PUT',
        headers: {
			'Content-type': 'application/json',
			'Authorization': localStorage.getItem('token')
        },
        body: order_detail
    })
        .then((response) => response.json())
        .then(function (data) {
			console.log(data);
		});
}

function resetOrderStatusTabs() {
	document.getElementById('new_order').innerHTML = '';
	document.getElementById('processing_order').innerHTML = '';
	document.getElementById('cancelled_order').innerHTML = '';
	document.getElementById('complete_order').innerHTML = '';
}