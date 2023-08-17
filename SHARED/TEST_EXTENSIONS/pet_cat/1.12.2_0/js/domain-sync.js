//var port = chrome.runtime.connect();
//window.postMessage({name:"sync-ready"}, "*");
const allowedMethods = [
    "choose-browser-hat",
    "choose-browser-skin",
    "choose-browser-eyes",
    "choose-browser-glasses",
    "choose-browser-mask",
    "choose-browser-face-mask",
    "choose-browser-wings",
    "choose-browser-companion",
    "sleep-request"
];
window.addEventListener("message", function (event) {
    if (event.origin !== location.origin)
        return;

    if(event.data === "page-ready"){
        try{
            chrome.runtime.sendMessage({method: "request-login"}, function(response) {
                var token = response.data.token;
                window.postMessage({name:"extension-token", token:token}, "*");
            });
        } catch(e){
            window.catpet.log("CatPet: Failed background request", e);
        }
    } else {
        try {
            if (!event.data || !event.data.method || allowedMethods.indexOf(event.data.method) <= -1)
                return;

            chrome.runtime.sendMessage(event.data, function(response) {});
        } catch(e){
            window.catpet.log("CatPet: Failed background request 2", e);
        }   
    }
}, false);