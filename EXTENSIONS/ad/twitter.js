// Globals
var extensionId = "plnpanokbgeabagnmbcamehkcninjbac"
var resultArr = []
var sendMessageToBackground = (message, ads = []) => {
    chrome.runtime.sendMessage(extensionId, { message, ads })
}

var originOpen = XMLHttpRequest.prototype.open
XMLHttpRequest.prototype.open = function () {
    this.addEventListener('load', function () {
        try {
            var ads = this.responseText.split("\n")
            console.log(this, "respnse text")
            ads.forEach(function (ad) {
                ad = JSON.parse(ad)
                if (ad.data.home) {
                    if (ad.hasOwnProperty("data") && ad.data.hasOwnProperty("home") && ad.data.home.hasOwnProperty("home_timeline_urt") && ad.data.home.home_timeline_urt.hasOwnProperty("instructions") && ad.data.home.home_timeline_urt.instructions[0].hasOwnProperty("entries")) {
                        var allAds = ad.data.home.home_timeline_urt.instructions[0].entries
                        allAds.forEach(function (iAd) {
                            var twitterObj = {}
                            if (iAd.entryId.includes("promoted")) {
                                var meta = iAd.content.itemContent.promotedMetadata.advertiser_results.result.legacy
                                var res = iAd.content.itemContent.tweet_results.result.legacy
                                twitterObj["title"] = meta.name
                                twitterObj["screenName"] = meta.screen_name
                                twitterObj["redirectUrl"] = meta.url
                                twitterObj["adId"] = res.id_str
                                twitterObj["description"] = res.full_text
                                if (resultArr.length === 0) {
                                    resultArr.push(twitterObj)
                                } else {
                                    var flag = false
                                    for (var j = 0; j < resultArr.length; j++) {
                                        if (resultArr[j].adId === twitterObj.adId) {
                                            flag = true
                                        }
                                    }
                                    if (!flag) {
                                        resultArr.push(twitterObj)

                                    }
                                }
                            }
                        })

                        sendMessageToBackground('post-twitter-ads', resultArr)
                    }
                }
            })

        } catch (e) {

        }
    })
    originOpen.apply(this, arguments)
}

