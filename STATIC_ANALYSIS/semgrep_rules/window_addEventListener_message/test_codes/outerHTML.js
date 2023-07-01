// Receiver.html
window.addEventListener("message", function(event) {
    if (event.source !== window.opener) {
      return; // Ignore messages from unknown sources
    }
  
    var outputDiv = document.getElementById("output");
    outputDiv.outerHTML = "Received Message: " + event.data; //match expected
  });
  
  function doggo(event){
    var outputDiv = document.getElementById("output");
    outputDiv.outerHTML = "Received Message: " + event.data; //match expected
  }
  window.addEventListener("message",doggo)
  window.addEventListener("message",doggo2)
  
  function doggo2(event){
    var outputDiv = document.getElementById("output");
    outputDiv.outerHTML = "Received Message: " + event.data; //match expected
  }