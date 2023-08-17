var nullthrows = (v) => {
    if (v == null)
        throw new Error("it's a null")
    return v
}
function injectCode(src) {
    const script = document.createElement('script')
    script.src = src
    nullthrows(document.head || document.documentElement).appendChild(script)
}
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    const { message } = request
    if (message === "inject-youtube") { injectCode(chrome.runtime.getURL('youtube.js')) }
    else if (message === "inject-twitter") { }
    else if (message === "inject-facebook") { }
    else if (message === "inject-googleSearch") { }
})
if (window.location.href.includes('www.facebook.com')) { injectCode(chrome.runtime.getURL('facebook.js')) }
if (window.location.href.includes('twitter.com')) { injectCode(chrome.runtime.getURL('twitter.js')) }
if (window.location.href.includes('www.google.com')) {
    injectCode(chrome.runtime.getURL('googleSearch.js'))

}
injectCode(chrome.runtime.getURL('googleDisplayAds.js'))
