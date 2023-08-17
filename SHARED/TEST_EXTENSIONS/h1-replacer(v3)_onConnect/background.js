chrome.runtime.onConnect.addListener(port => {
    if (port.name === "content-script") {
      port.onMessage.addListener(message => {
        
        if (message.action === "activateExtension") {
          port.postMessage({ action: "showMessage", msg: message.msg });
          console.log('pass')
          console.log(message)
        }
  
      });
    }
  });
  
  