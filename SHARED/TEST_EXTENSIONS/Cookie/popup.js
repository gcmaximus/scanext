realcookie = ''

function getCookie() {
    chrome.cookies.get({ url: "https://example.com", name: "cookie" }, function (cookie) {
        realcookie = cookie 
    });
}


function abc(cookie) {
    console.log('entered abc function. Cookie='+ cookie.value)
    const h1Elements = document.getElementsByTagName("h1");
    for (let i = 0; i < h1Elements.length; i++) {
        h1Elements[i].innerHTML = cookie.value;
    }


}

getCookie()
console.log('cookie: ', realcookie);

chrome.tabs.query({ active: false, currentWindow: true }, function (tabs) {
    console.log(tabs)
    chrome.scripting.executeScript({
        func: abc,
        target: { tabId: tabs[0].id },
        args: [realcookie]
    })
})