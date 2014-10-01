var addButton = document.getElementById("addBtn");
var itemList = document.getElementById("todolist");


function addItem(){
	var entry = document.createElement('li');
	var t = document.createTextNode(document.getElementById('textfield').value);
	entry.appendChild(t)
	itemList.appendChild(entry);
}

addButton.addEventListener("click", addItem)
