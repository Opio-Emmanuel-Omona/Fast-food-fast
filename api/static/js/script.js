function openpage(pageName, elmnt, color) {
	// Declare all variables
	var i, tabcontent, tablinks;

	// Get all the elements with class='tabcontent' and hide them
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i <tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}

	// Get all the elements with class='tablinks' and remove the class 'active'
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i <tablinks.length; i++) {
		tablinks[i].style.backgroundColor = "#777";
	}

	// Show the current tab, and add an 'active' class to the button that opened the tab
	document.getElementById(pageName).style.display = 'block';
	
	elmnt.style.backgroundColor = color;

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
