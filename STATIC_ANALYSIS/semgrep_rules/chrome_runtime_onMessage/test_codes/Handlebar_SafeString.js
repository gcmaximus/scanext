// content.js

// Receive message from background script
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    // Handle the message
    if (message.type === 'greeting') {
      const template = Handlebars.compile('<p>{{greeting}}</p>');
      const context = { greeting: new Handlebars.SafeString(message.greeting) };
      const html = template(context);
  
      // Inject the HTML into the page
      document.body.innerHTML += html;
    }
  });
  //1 matches to be found