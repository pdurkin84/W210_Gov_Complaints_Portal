var buddy311buttonClick = function () {
	console.log("Buddy311 button pressed");
	var results = document.getElementById('final_span');
	if (results.innerText == "" ) {
		console.log("final span empty, checking interim span");
		results = document.getElementById('interim_span');
	}
	if (results.innerText == "" ) {
		console.log("No text, ignoring");
		// for testing purposes remove the return here so that it continues to get classifications
		// return;
	}
	console.log("Received text: ", results.innerText);
	xhttp = new XMLHttpRequest();
	// Function called when data returns
	xhttp.onreadystatechange = function(d) {
		console.log("Statechange function called: ", this.responseText);
		if (this.responseText != "") {
			typeText = JSON.parse(this.responseText);
			console.log("The json value is : ", typeText);

			var typeLocation = document.getElementById('returnclass-type');
			var subtypeLocation = document.getElementById('returnclass-subtype');
			typeLocation.innerHTML="<strong><font color=\"red\"> Type: </font></strong>" + typeText['complaintType'];
			subtypeLocation.innerHTML="<strong> <font color=\"red\">Subtype: </font></strong>" + typeText['complaintSubtype'];
			typeLocation.style.visibility = "visible";
			subtypeLocation.style.visibility = "visible";
		}
	}
	xhttp.open("POST", "http://localhost:31101/buddy311/v0.1/", true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send('{ "description":"' + results.innerText + '" }');
}
