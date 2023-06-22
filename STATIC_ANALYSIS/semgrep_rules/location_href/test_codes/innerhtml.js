// content.js

// Retrieve the current URL using location.href
var currentURL = location.href;

// Create a new HTML element
var divElement = document.createElement('div');

// Set the innerHTML of the div element to the current URL
divElement.innerHTML = currentURL;

// Append the div element to the body of the webpage
document.body.appendChild(divElement);
