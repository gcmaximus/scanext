var extensionId = "plnpanokbgeabagnmbcamehkcninjbac"

var sendMessageToBackground = (message, ads = []) => {
    chrome.runtime.sendMessage(extensionId, { message, ads })
}

var waitUntilYoutubePlayerLoads = async () => {

    return await new Promise(resolve => {
        var interval = setInterval(() => {
            var playerContainer = document.querySelector(".qGXjvb")
            resolve(playerContainer)
            clearInterval(interval)

        }, 1000)
    })
}

(async () => {

    await waitUntilYoutubePlayerLoads()
    const resultArr = []

    let searchText = document.title
    let adsSelector = document.querySelector(".qGXjvb")
    let bottomAdsSelector = document.querySelector("#bottomads")

    if (adsSelector) {
        let ads = adsSelector.querySelectorAll(".uEierd")

        for (let i = 0; i < ads.length; i++) {
            let adData = {}

            let adsInnerBody = ads[i].querySelector(".d8lRkd")
            let tempAdName = adsInnerBody.querySelector(".BTu2cd")
            adData['position'] = i + 1
            // console.log('before adselector title')
            adData['searchText'] = searchText.slice(0, searchText.indexOf("-"))

            adData['adName'] = tempAdName.innerText
            adData['appearanceUrl'] = adsInnerBody.querySelector(".x2VHCd").innerText
            let tempRedirectUrl = document.querySelectorAll('.v5yQqb')
            adData['redirectUrl'] = tempRedirectUrl[i].querySelector("a").getAttribute('href')
            adData['title'] = document.querySelectorAll(".CCgQ5")[i].querySelector("span").innerText
            let tempDescription = document.querySelectorAll('.vdQmEd.fP1Qef.EtOod.pkphOe')
            adData['description'] = tempDescription[i].querySelector('.MUxGbd.yDYNvb.lyLwlc').innerText
            let imageUrl = ads[i].querySelector('.H9lube')?.querySelector('img')?.src ? ads[i].querySelector('.H9lube')?.querySelector('img')?.src : ""
            console.log('imageUrl-top ads', imageUrl)
            adData['favIcon'] = imageUrl

            let cta = []
            let ctaLink = []

            let ctaSelector = ads[i].querySelector(".UBEOKe")
            let ctaLinkSelector = ads[i].querySelector(".bOeY0b")

            let tempLinkCTA = ctaLinkSelector ? ads[i].querySelector(".bOeY0b").querySelectorAll("a") : ""

            for (let i = 0; i < tempLinkCTA?.length; i++) {
                let obj = {}
                let ctaLinkText = tempLinkCTA[i].innerText
                let ctaLinkHref = tempLinkCTA[i].href
                obj[ctaLinkText] = ctaLinkHref
                ctaLink.push(obj)
            }

            let tempCTA = ctaSelector ? ads[i].querySelector(".UBEOKe").querySelectorAll(".MhgNwc") : ""

            for (let i = 0; i < tempCTA?.length; i++) {
                let obj = {}
                let ctaTitle = tempCTA[i].querySelector(".MUxGbd").querySelector("a").innerText
                let ctaDescription = tempCTA[i].querySelector(".yDYNvb").innerText
                obj[ctaTitle] = ctaDescription
                cta.push(obj)
            }

            // if (cta.length > 0) {

            //     // console.log('cta true', cta.length)
            // }
            // else if (ctaLink.length > 0) {
            //     // console.log('ctaLink true', ctaLink)

            // }
            // else {
            //     console.log('else block')
            //     // adData['metaData'] = "no data"
            // }
            cta.length > 0 ? adData['metaData'] = cta : ctaLink.length > 0 ? adData['metaData'] = ctaLink : "null"

            resultArr.push(adData)
        }
        // console.log(resultArr, 'google-search-resultArr')
        sendMessageToBackground('post-googleSearch-ads', resultArr)
    }

    const bottomAdsresultArr = []
    if (bottomAdsSelector) {
        // console.log(resultArr.length)
        let topAdsLength = resultArr.length
        let bottomads = bottomAdsSelector.querySelectorAll(".uEierd")

        for (let i = 0; i < bottomads.length; i++) {
            let adData = {}
            let adsInnerBody = bottomads[i].querySelector(".d8lRkd")
            let tempAdName = adsInnerBody.querySelector(".BTu2cd")
            // console.log('tempAdName', tempAdName)
            let adLength = topAdsLength + 1
            adData['position'] = adLength
            adData['searchText'] = searchText.slice(0, searchText.indexOf("-"))
            topAdsLength = adLength
            adData['adName'] = tempAdName.innerText
            adData['appearanceUrl'] = temp1 = adsInnerBody.querySelector(".x2VHCd").innerText

            let tempRedirectUrl = bottomads[i].querySelector('.v5yQqb')
            adData['redirectUrl'] = temp2 = tempRedirectUrl.querySelector("a").getAttribute('href')

            adData['title'] = temp3 = bottomads[i].querySelector(".CCgQ5").querySelector("span").innerText

            let tempDescription = bottomads[i].querySelector('.vdQmEd.fP1Qef.EtOod.pkphOe')
            adData['description'] = temp4 = tempDescription.querySelector('.MUxGbd.yDYNvb.lyLwlc').innerText
            let imageUrl = bottomads[i].querySelector('.H9lube')?.querySelector('img')?.src ? bottomads[i].querySelector('.H9lube')?.querySelector('img')?.src : ""
            console.log('imageUrl-top ads', imageUrl)
            adData['favIcon'] = imageUrl

            let cta = []
            let ctaLink = []
            let ctaSelector = bottomads[i].querySelector(".UBEOKe")
            let ctaLinkSelector = bottomads[i].querySelector(".bOeY0b")
            let tempLinkCTA = ctaLinkSelector ? bottomads[i].querySelector(".bOeY0b").querySelectorAll("a") : ""

            for (let i = 0; i < tempLinkCTA?.length; i++) {
                let obj = {}
                let ctaLinkText = tempLinkCTA[i].innerText
                let ctaLinkHref = tempLinkCTA[i].href
                obj[ctaLinkText] = ctaLinkHref
                ctaLink.push(obj)

            }

            let tempCTA = ctaSelector ? bottomads[i].querySelector(".UBEOKe").querySelectorAll(".MhgNwc") : ""

            for (let i = 0; i < tempCTA?.length; i++) {
                let obj = {}
                let ctaTitle = tempCTA[i].querySelector(".MUxGbd").querySelector("a").innerText
                let ctaDescription = tempCTA[i].querySelector(".yDYNvb").innerText
                obj[ctaTitle] = ctaDescription
                cta.push(obj)
            }
            cta ? adData['metaData'] = cta : "null"
            ctaLink ? adData['metaData'] = ctaLink : "null"

            bottomAdsresultArr.push(adData)
        }
        // console.log(bottomAdsresultArr, 'bottom ads')
        sendMessageToBackground('post-googleSearch-ads', bottomAdsresultArr)
    }
})()

