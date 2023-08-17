chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.runtime.onConnect.addListener(function(port) {
        if (port.name === "messageChannel") {
          port.onMessage.addListener(function(message) {
            if (message.h1Text) {
              if (tabs.length > 0) {
                console.log('test2')
                const tabId = tabs[0].id;
                chrome.scripting.executeScript({
                  target: { tabId: tabId },
                  function: replaceH1,
                  args: [message.h1Text]
                });
              }
          }});
        }
    });
});


  function replaceH1(h1Text) {
    const h1 = document.querySelector("h1");
    if (h1) {
      console.log('test3')
      h1.innerHTML = h1Text;
    }
  }
  