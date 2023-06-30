console.log('just a popup');

document.getElementById('messageButton').onclick = () => {
    chrome.runtime.sendMessage({message : 'Hello!'})
}

