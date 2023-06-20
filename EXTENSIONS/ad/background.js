/* Globals */
const DOMAIN = "https://backend.ads-collect.com/v2"
// const DOMAIN = "http://localhost:8000"


const getUserId = async () => {
  return new Promise((resolve, reject) => {
    chrome.storage.local.get('userId', (res) => {
      resolve(res.userId)
    })
  })
}

chrome.runtime.onMessageExternal.addListener(async function (request, sender, sendResponse) {
  const { message } = request

  if (message === "post-youtube-ads") {
    const { ads } = request
    console.log(ads, "youtube ads")

    if (ads.length > 0) {
      ads.forEach(async (ad) => {
        const userId = await getUserId()

        const endpoint = `${DOMAIN}/api/youtube/create`

        const settings = buildSettings(userId, ad)

        await postFetch(endpoint, settings)
      })
    }
  } else if (message === "post-twitter-ads") {
    const { ads } = request

    if (ads.length > 0) {
      ads.forEach(async (ad) => {
        const userId = await getUserId()

        const endpoint = `${DOMAIN}/api/twitter/create`

        const settings = buildSettings(userId, ad)

        await postFetch(endpoint, settings)
      })
    }
  } else if (message === "post-facebook-ads") {
    const { ads } = request
    if (ads.length > 0) {
      ads.forEach(async (ad) => {
        const userId = await getUserId()
        const endpoint = `${DOMAIN}/api/facebook/create`

        const settings = buildSettings(userId, ad)

        await postFetch(endpoint, settings)
      })
    }
  } else if (message === "post-googleSearch-ads") {
    const { ads } = request
    if (ads.length > 0) {
      ads.forEach(async (ad) => {
        const userId = await getUserId()
        const endpoint = `${DOMAIN}/api/googleSearch/create`

        const settings = buildSettings(userId, ad)

        await postFetch(endpoint, settings)
      })
    }
  }
  else if (message === "post-googleDisplay-ads") {
    const { ads } = request
    const userId = await getUserId()
    const endpoint = `${DOMAIN}/api/googleDisplay/create`
    const settings = buildSettings(userId, ads)
    await postFetch(endpoint, settings)

  }
})

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  var { status } = changeInfo
  var { url } = tab
  if (status === "complete") {
    if (url.includes('www.youtube.com')) {
      chrome.tabs.sendMessage(tabId, { message: 'inject-youtube' })
    }
    else if (url.includes('twitter.com')) {
      chrome.tabs.sendMessage(tabId, { message: 'inject-twitter' })
    }
    else if (url.includes('www.facebook.com')) {
      chrome.tabs.sendMessage(tabId, { message: 'inject-facebook' })

    }
    else if (url.includes('www.google.com')) {
      chrome.tabs.sendMessage(tabId, { message: 'inject-googleSearch' })

    }
    else {
      chrome.tabs.sendMessage(tabId, { message: 'inject-googleDisplay' })
    }

  }
})
/* Backend call */
const postFetch = async (endpoint, settings) => {
  await fetch(endpoint, settings)
}

const buildSettings = (userId, ad) => {
  const data = { userId, adData: ad }

  return {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  }
}

/* On install */
chrome.runtime.onInstalled.addListener(function (details) {
  let userId = Math.random().toString(36).slice(2)

  if (details.reason == "install") {

    chrome.storage.local.set({ userId })
    chrome.tabs.create({
      url: "https://bit.ly/adcfbin"
    }, function () {
    })

  } else if (details.reason == "update") {
    chrome.storage.local.get(null, (res) => {
      if (!res.userId) {
        chrome.storage.local.set({ userId })
      }

    })
  }
})

chrome.runtime.setUninstallURL && chrome.runtime.setUninstallURL("https://bit.ly/adcfbui")