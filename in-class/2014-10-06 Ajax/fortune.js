var req;

var updateButton = document.getElementById("update_button");


function sendReq(){
	if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "http://garrod.isri.cmu.edu/webapps/fortune", true);
    req.send();
}

function handleResponse(){
	if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list items
    var content = document.getElementById("content");
    while (content.hasChildNodes()) {
        content.removeChild(content.firstChild);
    }

    // Parses the response to get a list of JavaScript objects for
    // the items.
    var item = JSON.parse(req.responseText);

    console.log(item["fortune"]);
    var newItem = document.createElement("p");
    var t = document.createTextNode(item["fortune"]);
    newItem.appendChild(t);
    content.appendChild(newItem);

}

updateButton.addEventListener("click", sendReq);
