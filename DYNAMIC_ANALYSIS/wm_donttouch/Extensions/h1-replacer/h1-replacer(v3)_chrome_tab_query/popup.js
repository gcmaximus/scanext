document.addEventListener('DOMContentLoaded', function() {
  var selectElement = document.getElementById('entryPoint');
  document.getElementById('submit').addEventListener('click', function() {
    var selectedValue = selectElement.value;
    selectedValue = parseInt(selectedValue)


    chrome.tabs.query({}, function(tabs) {
    });

      function changeH1Text() {
        chrome.tabs.query({ active: false, currentWindow: true }, function(tabs) {
          const activeTab = tabs[0];
          console.log(activeTab)

          possible_variables = ['favIconUrl', 'sessionId', 'title', 'url']
          
          var variable = 'Nil';
          switch (selectedValue) {
            case 0: // favIconUrl
              variable = activeTab.favIconUrl;
              break;
            case 1: // sessionId
              variable = activeTab.sessionId;
              break;
            case 2: // title
              variable = activeTab.title;
              break;
            case 3: // url
              variable = activeTab.url;
              break;
            default:
              variable = ""; // Default value if selectedValue is not one of the expected options
              break;
          }
          console.log(`Variable: ${possible_variables[selectedValue]} = ${variable}`)
      
          chrome.scripting.executeScript({
            target: { tabId: activeTab.id },
            function: modifyH1Elements,
            args: [variable]
          });
        });
      }
      
      function modifyH1Elements(content) {
        const h1Elements = document.getElementsByTagName('h1');
        for (let i = 0; i < h1Elements.length; i++) {
          h1Elements[i].innerHTML = content;
        }
      }
      changeH1Text()

  });
});



//  INSERT INTO EXAMPLE WEBSITE CODE:
// code: 'document.title = "New Title";'