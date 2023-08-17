
var extensionId = "plnpanokbgeabagnmbcamehkcninjbac"

let tempimgArray
let imgArray = document.querySelectorAll('iframe')

// window.onload = (event) => {
//     start()
// };

var sendDisplayAdsToBackground = (message, ads = {}) => {
    chrome.runtime.sendMessage(extensionId, { message, ads: ads['adData'] })
}

const delay = (imgArr) => {
    return new Promise(async (resolve) => {
        let displayAdObj = { 'adData': {} }

        let tempHref = imgArr?.contentDocument?.querySelector('#google_image_div a')?.getAttribute('href')

        if (tempHref) {
            displayAdObj.adData['redirectUrl'] = tempHref
        }
        let tempImgUrl = imgArr?.contentDocument?.querySelector('#google_image_div a')?.children[0]?.getAttribute('src')

        if (tempImgUrl) {
            displayAdObj.adData['imageUrl'] = tempImgUrl
        }

        if (tempImgUrl) {
            displayAdObj.adData['adId'] = tempImgUrl.slice(tempImgUrl.indexOf('simgad') + 7, (tempImgUrl.indexOf('?') ? tempImgUrl.indexOf('?') : tempImgUrl.indexOf('?') + 1))

        }

        if (tempHref && tempImgUrl) {
            console.log(displayAdObj, "display ads")
            await sendDisplayAdsToBackground('post-googleDisplay-ads', displayAdObj)
        }
        resolve()
    })
}

const doNextPromise = (d) => {
    delay(tempimgArray[d])

        .then(() => {
            d++;
            if (d < tempimgArray.length) {
                doNextPromise(d);
            }
            else {
            }
        })
}

const doPromise = (element) => {
    tempimgArray = element
    doNextPromise(0)
}

const untilIframeSelectorLoads = async (selec) => {
    return await new Promise((resolve, reject) => {
        const interval = setInterval(() => {
            let element = document.querySelectorAll(selec)
            let finalState = true

            if (element.length == 0) {

                finalState = false
            }

            if (finalState) {
                resolve()
                doPromise(element)
                clearInterval(interval)

            }
        }, 5000)
    })
}

const start = async () => {
    await untilIframeSelectorLoads('iframe')
}

window.addEventListener('load', function () {
    start()
})
