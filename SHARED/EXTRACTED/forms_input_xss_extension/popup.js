document.getElementById('replace-form').addEventListener('submit', async function (event) {
    event.preventDefault();
  
    const newText = document.getElementById('newText').value;
  
    try {
      let [tab] = await chrome.tabs.query({ active: false, currentWindow: true });
  
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: replaceH1s,
        args: [newText]
      });
    } catch (error) {
      console.log(error);
    }
  });
  
  function replaceH1s(newText) {
    const h1Tags = document.querySelectorAll('h1');
    for (const h1 of h1Tags) {
      h1.textContent = newText;
    }
  }
  