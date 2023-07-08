document.addEventListener('DOMContentLoaded', function () {
    var replacementInput = document.getElementById('replacementInput');
    var replaceButton = document.getElementById('replaceButton');


    replaceButton.addEventListener('click', function () {
      chrome.tabs.query({ active: false, currentWindow: true }, function (tabs) {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          function: replaceH1Tags,
          args: [replacementInput.value]
        }).then(() => {
          console.log(replacementInput.value)
          console.log('cao')
          // Handle success
        }).catch((error) => {
          // Handle error
          console.error(error);
        });
      });
    });
  });
  
  function replaceH1Tags(replacementText) {
    console.log(replacementText)
    console.log('cao2')


    var h1Tags = document.getElementsByTagName('h1');
    for (var i = 0; i < h1Tags.length; i++) {
      h1Tags[i].innerHTML = replacementText;
    }
    
  }
  