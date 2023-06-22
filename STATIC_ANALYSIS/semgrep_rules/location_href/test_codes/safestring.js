// content.js

// Retrieve the current URL using location.href
var currentURL = location.href;

// Create a new HTML element
var divElement = document.createElement('div');

// Create a Handlebars template string with the current URL
var templateString = '<span>{{{safeURL}}}</span>';

// Compile the Handlebars template
var template = Handlebars.compile(templateString);

// Create a safe version of the URL using Handlebars SafeString()
var safeURL = new Handlebars.SafeString(currentURL);

// Set the HTML content of the div element to the compiled template with the safe URL
divElement.innerHTML = template({ safeURL: safeURL });

// Prepend the div element to the body of the webpage
document.body.insertBefore(divElement, document.body.firstChild);
