document.addEventListener('DOMContentLoaded', function () {
    var messageButton = document.getElementById('messageButton');

    // Add click event listener to the button
    messageButton.addEventListener('click', function () {
        // Send a message to the background script
        chrome.runtime.sendMessage({
            message: 'Button clicked!'
        });
    });
});

window.addEventListener('message', function (event) {
    // Handle messages received from other sources
    console.log("Message received in popup:", event.data);
});
