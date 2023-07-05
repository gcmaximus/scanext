chrome.runtime.onMessage.addListener(message => {
    if (message.type === "updateH1") {
      const h1Element = document.querySelector("h1");
      if (h1Element) {
        h1Element.innerHTML = message.text;
      }
    }
  });
  