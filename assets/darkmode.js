'use strict'

// Selecting the required elements as well as the localStorage for the theme 
const input = document.querySelector(".slider");
const currentTheme = localStorage.getItem("theme");
	
if (currentTheme === "dark") {
  	document.body.classList.add("dark-theme");
}

// OnClick event being handled 
input.addEventListener("click", function (e) {
	document.body.classList.toggle("dark-theme");
	
	let theme = "light";
	if (document.body.classList.contains("dark-theme")) {
		theme = "dark";
 }
	localStorage.setItem("theme", theme);
});