// popup.js

// Version 1

function displayUrl(tabInfo) {
  console.log(tabInfo)
  document.getElementById('url').innerHTML = tabInfo[0].url
}

var gettingCurrent = chrome.tabs.query({active: true, currentWindow: true});
// var gettingCurrent = chrome.tabs.getCurrent()
// gettingCurrent.then(displayUrl, onError)
gettingCurrent.then((tab) => {
  displayUrl(tab)
})

// Version 2

// document.addEventListener('DOMContentLoaded', function() {
//   chrome.tabs.getCurrent(function(tab) {
//     // Use tab object to access current tab information
//     var currentTabUrl = tab.url;

//     // Display the current tab information in the popup.html
//     var tabUrlElement = document.getElementById('url');

//     tabUrlElement.innerHTML = 'Tab URL: ' + currentTabUrl;
//   });
// });

// Version 3

// function onGot(tabInfo) {
//   console.log(tabInfo);
// }

// function onError(error) {
//   console.log(`Error: ${error}`);
// }

// var gettingCurrent = chrome.tabs.getCurrent();
// gettingCurrent.then(onGot, onError);

