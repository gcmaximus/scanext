function displayMessage() {
    var unsafeInput = window.name;
    document.getElementById('displayArea').innerHTML = unsafeInput;
    document.getElementById('displayArea').outerHTML = unsafeInput;
}