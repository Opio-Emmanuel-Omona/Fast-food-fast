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
	if (pageName == 'Orders') {
		getOrders();
	}
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

	//update the status of the order
	updateOrderStatus(data, ev.target.id)
}

function dropFile(ev) {
	ev.preventDefault();
	document.getElementById('item_name').value = ev.dataTransfer.files[0]['name'].split('.')[0];
	ev.target.innerHTML = 'Succesfully dropped';
	upload(ev.dataTransfer.files[0]);
}

function changeColor(ev) {
	ev.preventDefault();
	ev.target.className = "dropzone dragover";
}

function changeColorBack(ev) {
	ev.preventDefault();
	ev.target.className = "dropzone";
}

function upload(file) {
	url = 'http://fast-food-fast-op.herokuapp.com/upload';

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-type': 'application/json',
			'Authorization': localStorage.getItem('token')
		},
		body: file
	})
		.then((response) => response.json())
		.then(function (data) {
			console.log(data);
		})
}

function getOrders() {
	// get all the orders and display them according to status
	url = 'http://fast-food-fast-op.herokuapp.com/api/v2/orders';

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

			if (data['orders']) {
				for (let index = 0; index < data['orders'].length; index++) {
					let output = `
						<div id="${data['orders'][index].order_id}" draggable="true" ondragstart="drag(event)" class="content-section-b">
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
						// error
					}
				}
			}
			else {
				// error
				if (confirm('Session timeout\n log in as admin')){
					url = "http://fast-food-fast-op.herokuapp.com/login"
					window.location.href = url;
				}
				
			}

		});
}

function fetchSpecificOrder() {

	// get a specific order and display it
	url = 'http://fast-food-fast-op.herokuapp.com/api/v2/orders/' + document.getElementById('searchField').value;

	fetch(url, {
		method: 'GET',
		headers: {
			'Content-type': 'application/json',
			'Authorization': localStorage.getItem('token')
		},
	})
		.then((response) => response.json())
		.then(function (data) {

			var output = '';
			if (data['order'][0]) {
				console.log(data);
				output = `Order ID: ${data['order'][0].order_id}<br>
						  Username: ${data['order'][0].username}<br>
						  Item Name: ${data['order'][0].item_name}<br>
						  Quantity: ${data['order'][0].quantity}<br>`
			}
			else {
				console.log(data)
				document.getElementById('searchResult').style.className = 'error';
				output = "Order Doesn't exist";
			}
			document.getElementById('searchResult').style.display = 'block';
			document.getElementById('searchResult').innerHTML = output;
		});

}

function addItem(e) {
	e.preventDefault();

	url = 'http://fast-food-fast-op.herokuapp.com/api/v2/menu';

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
			console.log(data['message']);
			if (data['message'].includes('succes')) {
				document.getElementById('validityOK').innerHTML = 'OK';
				document.getElementById('validityBad').innerHTML = '';
			}
			else {
				document.getElementById('validityBad').innerHTML = data['message'];
				document.getElementById('validityOK').innerHTML = '';
				console.log(data['message']);
			}
		});
}

function updateOrderStatus(orderId, newStatus) {
	url = 'http://fast-food-fast-op.herokuapp.com/api/v2/orders/' + orderId;


	if (newStatus.includes('new')) {
		newStatus = 'New';
	}
	else if (newStatus.includes('processing')) {
		newStatus = 'Processing';
	}
	else if (newStatus.includes('cancel')) {
		newStatus = 'Cancelled';
	}
	else if (newStatus.includes('complete')) {
		newStatus = 'Completed';
	}

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