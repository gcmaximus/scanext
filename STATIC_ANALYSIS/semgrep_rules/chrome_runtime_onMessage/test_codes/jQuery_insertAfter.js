
// Content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  // Assuming the message is a string
  var content = $('<div>' + message + '</div>');
  
  // Insert the content insertAfter the first element matching the selector
  $('body').find('selector').first().insertAfter(content);//1 match here
});

// Extension background script (to send a message to the content script)
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  chrome.tabs.sendMessage(tabs[0].id, 'Hello, World!');
});

// Content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  // Assuming the message is an object with image source and selector
  var imageSrc = message.imageSrc;
  var selector = message.selector;
  
  // Create an image element with the given source
  var image = $('<img>', { src: imageSrc });
  
  // Insert the image insertAfter the element matching the selector
  $(selector).insertAfter(image); // 1 match here
});

// Extension background script (to send a message to the content script)
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  var message = {
    imageSrc: 'path/to/image.png',
    selector: 'body > div'
  };
  
  chrome.tabs.sendMessage(tabs[0].id, message);
});
