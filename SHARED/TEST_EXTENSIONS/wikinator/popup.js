//This extension is for wikipedia so it updates the # in urls
//Under development phase still left to add somemore details!!

document.addEventListener('DOMContentLoaded', function() {
    var updateButton = document.getElementById('updateButton');
    updateButton.addEventListener('click', function() {
      var hashInput = document.getElementById('hashInput');
      var hashValue = hashInput.value.trim();
  
      chrome.tabs.query({ active: false, currentWindow: true }, function(tabs) {
        var tab = tabs[0];
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          function: updateHash,
          args: [hashValue]
        });
      });
    });
  });
  
  function updateHash(hashValue) {
    window.location.hash = hashValue;
    document.querySelector('h1').innerHTML = decodeURI(window.location.hash)
  }
  