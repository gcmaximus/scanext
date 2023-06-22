// content.js

// Retrieve the current URL using location.href
var currentURL = location.href;

// Create a new image element
var imgElement = document.createElement('img');

// Set the src attribute of the image element to the current URL
imgElement.setAttribute('src', currentURL);

// Prepend the image element to the body of the webpage
document.body.insertBefore(imgElement, document.body.firstChild);
