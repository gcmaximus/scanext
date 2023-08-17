var extensionId = "plnpanokbgeabagnmbcamehkcninjbac"

var waitUntilYoutubePlayerLoads = async () => {
    return await new Promise(resolve => {
        var interval = setInterval(() => {
            var playerContainer = document.querySelectorAll(".style-scope ytd-player")
            var finalState = false
            if (playerContainer.length > 0) {
                finalState = true
            }
            if (finalState == true) {
                resolve(playerContainer)
                clearInterval(interval)
            }
        }, 1000)
    })
}
var removeDuplicates = (duplicates) => {
    var flag = {}
    var unique = []
    duplicates.forEach(elem => {
        if (!flag[elem.adId]) {
            flag[elem.adId] = true
            unique.push(elem)
        }
    })
    return unique
}

var sendMessageToBackground = (message, ads = []) => {
    chrome.runtime.sendMessage(extensionId, { message, ads })
}

(async () => {
    var playerContainer = await waitUntilYoutubePlayerLoads()
    var mainElement

    // Determine the main element
    if (playerContainer.length === 2) {
        /* Handler if the container has two elements */
        var firstElement = playerContainer[0]
        var secondElement = playerContainer[1]


        if (secondElement.hasOwnProperty("_host") && secondElement._host.hasOwnProperty("__data") && secondElement._host.__data.hasOwnProperty("playerData") && secondElement._host.__data.playerData.hasOwnProperty("adPlacements")) {
            mainElement = secondElement
        } else if (firstElement.hasOwnProperty("_host") && firstElement._host.hasOwnProperty("__data") && firstElement._host.__data.hasOwnProperty("playerData") && firstElement._host.__data.playerData.hasOwnProperty("adPlacements")) {
            mainElement = firstElement
        }
    } else if (playerContainer.length === 1) {
        mainElement = playerContainer[0]
    }

    // Scrap data out of the main element
    if (mainElement.hasOwnProperty("_host") && mainElement._host.hasOwnProperty("__data") && mainElement._host.__data.hasOwnProperty("playerData") && mainElement._host.__data.playerData.hasOwnProperty("adPlacements")) {
        /* Handler for second element in the container */
        var content = mainElement._host.__data.playerData
        var adsArr = content.adPlacements
        var resultingArr = []

        for (var i = 0; i < adsArr.length; i++) {
            var iAd = adsArr[i]

            if (iAd.hasOwnProperty("adPlacementRenderer") && iAd.adPlacementRenderer.hasOwnProperty("renderer") && iAd.adPlacementRenderer.renderer.hasOwnProperty("actionCompanionAdRenderer")) {

                var acar = iAd.adPlacementRenderer.renderer.actionCompanionAdRenderer
                var resultingObj = {}
                resultingObj["title"] = acar.hasOwnProperty("headline") && acar.headline.text
                resultingObj["landingDomain"] = acar.hasOwnProperty("description") && acar.description.text
                resultingObj["adId"] = acar.hasOwnProperty("adVideoId") && acar.adVideoId
                resultingObj["adUrl"] = `https://www.youtube.com/embed/${resultingObj.adId}`
                resultingObj && resultingArr.push(resultingObj)

            }
        }
        console.log(resultingArr, 'youtube-resultingArr')
        // Filter the ads
        var filtered = removeDuplicates(resultingArr)
        // Send message to background
        sendMessageToBackground('post-youtube-ads', filtered)
    }
})()

//scrapping script old

// var extensionId = "plnpanokbgeabagnmbcamehkcninjbac"

// var waitUntilYoutubePlayerLoads = async () => {
//     return await new Promise(resolve => {
//         var interval = setInterval(() => {
//             var playerContainer = document.querySelectorAll(".style-scope ytd-player")
//             // console.log("playerContainer", playerContainer)
//             var finalState = false
//             if (playerContainer.length > 0) {
//                 finalState = true
//             }
//             if (finalState == true) {
//                 resolve(playerContainer)
//                 clearInterval(interval)
//             }
//         }, 1000)
//     })
// }
// var removeDuplicates = (duplicates) => {
//     var flag = {}
//     var unique = []
//     duplicates.forEach(elem => {
//         if (!flag[elem.adId]) {
//             flag[elem.adId] = true
//             unique.push(elem)
//         }
//     })
//     return unique
// }

// var sendMessageToBackground = (message, ads = []) => {
//     chrome.runtime.sendMessage(extensionId, { message, ads })
// }

// (async () => {
//     var playerContainer = await waitUntilYoutubePlayerLoads()
//     // console.log(playerContainer, 'playerContainer playerContainer')
//     var mainElement

//     // Determine the main element
//     if (playerContainer.length === 2) {
//         /* Handler if the container has two elements */
//         var firstElement = playerContainer[0]
//         var secondElement = playerContainer[1]

//         // console.log(firstElement, 'firstElement firstElement firstElement')


//         if (secondElement.hasOwnProperty("_host") && secondElement._host.hasOwnProperty("__data") && secondElement._host.__data.hasOwnProperty("playerData") && secondElement._host.__data.playerData.hasOwnProperty("adPlacements")) {
//             mainElement = secondElement
//         } else if (firstElement.hasOwnProperty("_host") && firstElement._host.hasOwnProperty("__data") && firstElement._host.__data.hasOwnProperty("playerData") && firstElement._host.__data.playerData.hasOwnProperty("adPlacements")) {
//             mainElement = firstElement
//         }
//     } else if (playerContainer.length === 1) {
//         mainElement = playerContainer[0]
//     }

//     console.log(mainElement, 'mainElement mainElement mainElement')
//     // Scrap data out of the main element
//     if (mainElement.hasOwnProperty("_host") && mainElement._host.hasOwnProperty("__data") && mainElement._host.__data.hasOwnProperty("playerData") && mainElement._host.__data.playerData.hasOwnProperty("adPlacements")) {
//         /* Handler for second element in the container */
//         var content = mainElement._host.__data.playerData
//         var adsArr = content.adPlacements
//         var resultingArr = []

//         for (var i = 0; i < adsArr.length; i++) {
//             var iAd = adsArr[i]

//             if (iAd.hasOwnProperty("adPlacementRenderer") && iAd.adPlacementRenderer.hasOwnProperty("renderer") && iAd.adPlacementRenderer.renderer.hasOwnProperty("actionCompanionAdRenderer")) {

//                 var acar = iAd.adPlacementRenderer.renderer.actionCompanionAdRenderer
//                 var resultingObj = {}
//                 resultingObj["title"] = acar.hasOwnProperty("headline") && acar.headline.text
//                 resultingObj["landingDomain"] = acar.hasOwnProperty("description") && acar.description.text
//                 resultingObj["adId"] = acar.hasOwnProperty("adVideoId") && acar.adVideoId
//                 resultingObj["adUrl"] = `https://www.youtube.com/embed/${resultingObj.adId}`
//                 resultingObj && resultingArr.push(resultingObj)

//             } else if (iAd.hasOwnProperty("adPlacementRenderer") && iAd.adPlacementRenderer.hasOwnProperty("renderer") && iAd.adPlacementRenderer.renderer.hasOwnProperty("linearAdSequenceRenderer") && iAd.adPlacementRenderer.renderer.linearAdSequenceRenderer.hasOwnProperty("linearAds")) {

//                 var linArr = iAd.adPlacementRenderer.renderer.linearAdSequenceRenderer.linearAds

//                 for (var k = 0; k < linArr.length; k++) {
//                     var resultingObj = {}
//                     if (linArr[k].hasOwnProperty("instreamVideoAdRenderer")) {
//                         var iLAd = linArr[k].instreamVideoAdRenderer;
//                         resultingObj["adId"] = iLAd.hasOwnProperty("externalVideoId") && iLAd.externalVideoId
//                         resultingObj["adUrl"] = `https://www.youtube.com/embed/${resultingObj.adId}`
//                         resultingObj && resultingArr.push(resultingObj)
//                     }
//                 }

//             } else if (iAd.hasOwnProperty("adPlacementRenderer") && iAd.adPlacementRenderer.hasOwnProperty("renderer") && iAd.adPlacementRenderer.renderer.hasOwnProperty("instreamVideoAdRenderer")) {

//                 var resultingObj = {}
//                 var acar = iAd.adPlacementRenderer.renderer.instreamVideoAdRenderer
//                 resultingObj["adId"] = acar.hasOwnProperty("externalVideoId") && acar.externalVideoId
//                 resultingObj["adUrl"] = `https://www.youtube.com/embed/${resultingObj.adId}`
//                 resultingObj && resultingArr.push(resultingObj)

//             } else if (iAd.hasOwnProperty("adPlacementRenderer") && iAd.adPlacementRenderer.hasOwnProperty("renderer") && iAd.adPlacementRenderer.renderer.hasOwnProperty("adsEngagementPanelRenderer")) {

//                 var acar = iAd.adPlacementRenderer.renderer.adsEngagementPanelRenderer
//                 var resultingObj = {}
//                 resultingObj["adId"] = acar.hasOwnProperty("adVideoId") && acar.adVideoId
//                 resultingObj["adUrl"] = `https://www.youtube.com/embed/${resultingObj.adId}`
//                 resultingObj && resultingArr.push(resultingObj)

//             }
//         }
//         console.log(resultingArr, 'youtube-resultingArr')
//         // Filter the ads
//         var filtered = removeDuplicates(resultingArr)
//         // Send message to background
//         sendMessageToBackground('post-youtube-ads', filtered)
//     }
// })()


