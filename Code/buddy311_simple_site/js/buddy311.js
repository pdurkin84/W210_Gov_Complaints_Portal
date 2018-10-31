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
		if (this.readyState != 4 ) {
			// State is not done
			return;
		}
		console.log("Statechange function called: ", this.responseText);
		if (this.responseText != "") {
			typeText = JSON.parse(this.responseText);
			console.log("The json value is : ", typeText);

			var fspan = document.getElementById('final_span');
			fspan.innerHTML+="<br><p><br><strong><font color=\"red\"> Type: </font>" + typeText['service_code'] + "</strong>";
		//	var typeLocation = document.getElementById('returnclass-type');
		//	typeLocation.innerHTML="<strong><font color=\"red\"> Type: </font></strong>" + typeText['service_code'];
		//	typeLocation.style.visibility = "visible";
		}
	}
	xhttp.open("POST", "https://buddy311.org:31102/buddy311/v0.1/", true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send('{ "description":"' + results.innerText + '", "service_code": "unknown" }');
}
