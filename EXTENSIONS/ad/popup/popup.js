var DOMAIN = "https://backend.ads-collect.com/v2"
//var DOMAIN = "http://localhost:8000"

var getUserId = async () => {
  return new Promise((resolve, reject) => {
    chrome.storage.local.get('userId', (res) => {
      resolve(res.userId)

    })

  })
}
var fetchFbAds = async (pageNo) => {
  var userId = await getUserId();

  await fetch(`${DOMAIN}/api/facebook/ads`,
    {
      headers: { 'Content-Type': "application/json", 'Accept': "application/json" },
      method: "POST",
      body: JSON.stringify({ userId, page: pageNo })
    }
  ).then(Response => Response.json()).then(fbAds => {

    totalfbads.innerText = fbAds.totalFacebookAdsCount;
  })
}
var fetchTwAds = async (pageNo) => {
  var userId = await getUserId();
  await fetch(`${DOMAIN}/api/twitter/ads`,
    {
      headers: { 'Content-Type': "application/json", 'Accept': "application/json" },
      method: "POST",
      body: JSON.stringify({ userId, page: pageNo })
    }
  ).then(Response => Response.json()).then(twAds => {

    totaltwiads.innerText = twAds.totalTwitterAdsCount;
  })
}
var fetchYtAds = async (pageNo) => {
  var userId = await getUserId();
  await fetch(`${DOMAIN}/api/youtube/ads`,
    {
      headers: { 'Content-Type': "application/json", 'Accept': "application/json" },
      method: "POST",
      body: JSON.stringify({ userId, page: pageNo })
    }
  ).then(Response => Response.json()).then(ytAds => {

    totalyouads.innerText = ytAds.totalYoutubeAdsCount;
  })
}
var fetchGsAds = async (pageNo) => {
  var userId = await getUserId();
  await fetch(`${DOMAIN}/api/googleSearch/ads`,
    {
      headers: { 'Content-Type': "application/json", 'Accept': "application/json" },
      method: "POST",
      body: JSON.stringify({ userId, page: pageNo })
    }
  ).then(Response => Response.json()).then(gsAds => {

    totalgsads.innerText = gsAds.totalGoogleSearchAdsCount;
  })
}
var fetchGdAds = async (pageNo) => {
  var userId = await getUserId();
  await fetch(`${DOMAIN}/api/googleDisplay/ads`,
    {
      headers: { 'Content-Type': "application/json", 'Accept': "application/json" },
      method: "POST",
      body: JSON.stringify({ userId, page: pageNo })
    }
  ).then(Response => Response.json()).then(gdAds => {

    totalgdads.innerText = gdAds.totalGoogleDisplayAdsCount;
  })
}


let totalfbads = document.querySelector(".totalfbads")
let totaltwiads = document.querySelector(".totaltwiads")
let totalyouads = document.querySelector(".totalyouads")
let totalgsads = document.querySelector(".totalgsads")
let totalgdads = document.querySelector(".totalgdads")


let today = new Date().toLocaleString().split(', ')[0]


fetchYtAds(1)
fetchTwAds(1)
fetchFbAds(1)
fetchGsAds(1)
fetchGdAds(1)

let viewCollectedAdsButton = document.querySelector(".bottom button")

viewCollectedAdsButton.addEventListener("click", () => {
  chrome.tabs.create({ url: chrome.runtime.getURL('index.html') })
})