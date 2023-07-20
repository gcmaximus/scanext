document.addEventListener('DOMContentLoaded', function() {
  var selectElement = document.getElementById('entryPoint');
  document.getElementById('submit').addEventListener('click', function() {
    var selectedValue = selectElement.value;
    selectedValue = parseInt(selectedValue);

    chrome.tabs.query({ active: false, currentWindow: true }, function(tabs) {
      const activeTab = tabs[0];
      console.log(activeTab);

      possible_variables = ['favIconUrl', 'sessionId', 'title', 'url'];
      var variable = 'Nil';

      switch (selectedValue) {
        case 1: // sessionId
          variable = activeTab.sessionId;
          break;
        case 2: // title
          variable = activeTab.title;
          break;
        case 0: // favIconUrl
          variable = activeTab.favIconUrl;
          break;
        case 3: // url
          variable = activeTab.url;
          break;
        default:
          variable = ""; // Default value if selectedValue is not one of the expected options
          break;
      }


      // if (selectedValue == 1)
      //     variable = activeTab.sessionId;
      // else if(selectedValue == 2)
      //     variable = activeTab.title;
      // else if(selectedValue == 2)
      //     variable = activeTab.favIconUrl;
      // else if(selectedValue == 2)
      //     variable = activeTab.url;
      // else
      //     variable = ""; // Default value if selectedValue is not one of the expected options
      
      
      

      console.log(`Variable: ${possible_variables[selectedValue]} = ${variable}`);

      const h1Elements = document.getElementsByTagName('h1');
      for (let i = 0; i < h1Elements.length; i++) {
        h1Elements[i].innerHTML = variable;
      }
    });
  });
});
