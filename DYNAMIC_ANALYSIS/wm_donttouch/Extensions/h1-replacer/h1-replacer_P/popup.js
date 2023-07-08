document.addEventListener("DOMContentLoaded", function () {
    var replacementInput = document.getElementById("replacementInput");
    var replaceButton = document.getElementById("replaceButton");

    replaceButton.addEventListener("click", function () {
        chrome.tabs.query(
            { active: false, currentWindow: true },
            function (tabs) {
                chrome.tabs.executeScript(tabs[0].id, {
                    code:
                        "var h1Tags = document.getElementsByTagName('h1'); for (var i = 0; i < h1Tags.length; i++) { h1Tags[i].innerHTML = '" +
                        replacementInput.value +
                        "'; }",
                });
            }
        );
    });
});
