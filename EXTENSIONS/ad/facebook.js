var extensionId = "plnpanokbgeabagnmbcamehkcninjbac"
console.log('facebook script injected')
function type_one(typename, typename2, creative, content) {
    var image_url;
    var image_width;
    var image_height;
    var raw_cta_url;
    var title;
    var body;
    if (typename === 'StoryAttachmentPhotoStyleRenderer' || typename2 === 'StoryAttachmentPhotoStyleRenderer') {
        image_url = creative["media"]["photo_image"]["uri"]
        image_width = creative["media"]["photo_image"]["width"]
        image_height = creative["media"]["photo_image"]["height"]
        raw_cta_url = ''
        title = ''
        body = ''
    } else {
        var image = creative["media"]["flexible_height_share_image"] || creative["media"]["large_share_image"] || creative["media"]["image"] || creative["media"]["photo_image"];
        image_url = image["uri"]
        image_width = image["width"]
        image_height = image["height"]
        if (content["story"]["attachments"][0]["comet_footer_renderer"]) {
            raw_cta_url = content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["target"]["external_url"]
            title = content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["title_with_entities"]["text"]
            body = content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["description"]["text"]
        }
    }
    return { image_url: image_url, image_width: image_width, image_height: image_height, raw_cta_url: raw_cta_url, title: title, body: body }
}

function type_two(creative) {
    var video_preview_image_url = creative["media"]["thumbnailImage"] ? creative["media"]["thumbnailImage"]["uri"] : creative["media"]["photo_image"]["uri"]
    var video_url = creative["media"]["playable_url_quality_hd"] ? creative["media"]["playable_url_quality_hd"] : creative["media"]["playable_url"];
    var video_id = creative["media"]["videoId"];

    return { video_preview_image_url: video_preview_image_url, video_url: video_url, video_id: video_id }
}

function type_three(creative_subattachments) { // è½®æ’­å›¾ç±»åž‹
    var card_list = []
    var subattachments = creative_subattachments
    var flag = 0;
    subattachments.forEach(subattachment => {
        var creative_url;
        if (subattachment["multi_share_media_card_renderer"]["attachment"]["media"]["__typename"] === "Video") {
            creative_url = subattachment["multi_share_media_card_renderer"]["attachment"]["media"]["playable_url"]
            flag = 1;
        } else {
            creative_url = subattachment["multi_share_media_card_renderer"]["attachment"]["media"]["image"] ? subattachment["multi_share_media_card_renderer"]["attachment"]["media"]["image"]["uri"] : ""
        }

        var _d = {
            title: subattachment["card_title"]["text"],
            body: subattachment["card_description"]["text"],
            creative_url: creative_url
        }
        if (subattachment["story_attachment_link_renderer"]["attachment"]["web_link"]) {
            _d.raw_cta_url = subattachment["story_attachment_link_renderer"]["attachment"]["web_link"]["url"]
        }
        var call_to_action_renderer = subattachment["call_to_action_renderer"]
        if (call_to_action_renderer) {
            _d.cta_text = subattachment["call_to_action_renderer"]["action_link"]["title"]
            _d.cta_type = subattachment["call_to_action_renderer"]["action_link"]["link_type"]
        }
        card_list.push(_d)
    })
    return { card_list: card_list, flag: flag }
}

function type_four(creative_nodes) {
    var type_four_list = []
    var type_four_nodes = creative_nodes
    type_four_nodes.forEach(node => {
        type_four_list.push(node["media"]["image"]["uri"])
    })
    return type_four_list
}

function type_five(creative_nodes) {
    var type_five_list = []
    var type_five_nodes = creative_nodes

    type_five_nodes.forEach(node => {
        type_five_list.push(node["media"]["image"]["uri"])
    })
    return type_five_list;
}

function analysisPostData(post_raw_data) {
    var data = {}

    if (post_raw_data.data.category === "SPONSORED") {
        var content = post_raw_data["data"]["node"]["comet_sections"]["content"]
        var comet_sections = post_raw_data["data"]["node"]["comet_sections"]
        var creative = content["story"]["attachments"][0]["styles"]["attachment"]
        var __typename = creative['media'] ? creative['media']['__typename'] : null
        var __typename2 = content["story"]["attachments"][0]["styles"]['__typename']
        if (__typename === 'StoryAttachmentMultiShareStyleRenderer' || __typename2 === 'StoryAttachmentMultiShareStyleRenderer') { // è½®æ’­å›¾ç±»åž‹
            var res = type_three(creative["subattachments"])
            data['card_list'] = res.card_list
            var flag = res.flag;
            if (flag === 1) {
                data["is_video"] = 1
            }
            data['type'] = 3
        } else if (__typename === "StoryAttachmentAlbumFrameStyleRenderer" || __typename2 === "StoryAttachmentAlbumFrameStyleRenderer") {
            data['image_list'] = type_five(creative[Object.keys(creative)[Object.keys(creative).length - 1]]["nodes"])
            data['type'] = 5
        } else if (__typename === 'StoryAttachmentAlbumStyleRenderer' || __typename2 === 'StoryAttachmentAlbumStyleRenderer') {
            data['image_list'] = type_four(creative["all_subattachments"]["nodes"])
            data['type'] = 4
        } else if (__typename === 'Video' || __typename2 === "Video") {
            var type_two_res = type_two(creative)
            data['video_preview_image_url'] = type_two_res.video_preview_image_url
            data["video_url"] = type_two_res.video_url
            data["video_id"] = type_two_res.video_id
            data['type'] = 2
        } else {
            data['type'] = 1
            var type_one_res = type_one(__typename, __typename2, creative, content)
            data['image_url'] = type_one_res.image_url
            data['image_width'] = type_one_res.image_width
            data['image_height'] = type_one_res.image_height
            data['raw_cta_url'] = type_one_res.raw_cta_url
            data["title"] = type_one_res.title
            data["body"] = type_one_res.body
        }

        if (content["story"]["attachments"][0]["comet_footer_renderer"]) {
            var action_link = content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["action_links"][0]
            if (data['type'] !== 1) {
                data['raw_cta_url'] = action_link["url"]
                data['title'] = action_link["link_title"]
                data['body'] = action_link["link_description"]
                data['media'] = action_link["link_display"]
            }
            var page_temp = comet_sections["context_layout"]["story"]["comet_sections"]["actor_photo"]["story"]["actors"][0]
            if (action_link && "__typename" in action_link && action_link["__typename"] === "MessagePageActionLink") {
                data["raw_cta_url"] = "https://www.facebook.com/" + page_temp["id"]
            }
        }
        data['comment_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]['comment_count']["total_count"];
        data['like_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]["reaction_count"]["count"]
        data['share_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]["share_count"]["count"]
        if (data['type'] === 2) {
            data['view_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]["video_view_count"]
        }
        var _message = content["story"]["comet_sections"]["message"]
        data['message'] = _message == null ? null : _message["story"]["message"]["text"]
        if (content["story"]["attachments"][0]["comet_footer_renderer"] && content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["call_to_action_renderer"]) {
            var cta = content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["call_to_action_renderer"]["action_link"]
            data['cta_text'] = cta["title"]
            data['cta_type'] = cta["link_type"]
        } else {
            data['cta_text'] = ''
            data['cta_type'] = ''
        }
        var page = comet_sections["context_layout"]["story"]["comet_sections"]["actor_photo"]["story"]["actors"][0]
        // page
        data['page_id'] = page["id"]
        data['page_name'] = page["name"]
        data['page_profile_url'] = page["profile_url"]
        data['post_id'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']['subscription_target_id']
    } else {
        var content = post_raw_data['data']["viewer"]["news_feed"]["edges"][0]['node']['comet_sections']["content"]
        var comet_sections = post_raw_data['data']["viewer"]["news_feed"]["edges"][0]['node']['comet_sections']
        var creative = content["story"]["attachments"][0]["styles"]["attachment"]
        var __typename = creative['media'] ? creative['media']['__typename'] : null
        var __typename2 = content["story"]["attachments"][0]["styles"]['__typename']
        if (__typename === 'StoryAttachmentMultiShareStyleRenderer' || __typename2 === 'StoryAttachmentMultiShareStyleRenderer') {
            var res = type_three(creative["subattachments"])
            data['card_list'] = res.card_list
            var flag = res.flag;
            if (flag === 1) {
                data["is_video"] = 1
            }
            data['type'] = 3
        } else if (__typename === "StoryAttachmentAlbumFrameStyleRenderer" || __typename2 === "StoryAttachmentAlbumFrameStyleRenderer") {
            data['image_list'] = type_five(creative[Object.keys(creative)[Object.keys(creative).length - 1]]["nodes"])
            data['type'] = 5
        } else if (__typename === 'StoryAttachmentAlbumStyleRenderer' || __typename2 === "StoryAttachmentAlbumStyleRenderer") {
            data['image_list'] = type_four(creative["all_subattachments"]["nodes"])
            data['type'] = 4
        } else if (__typename === 'Video' || __typename2 === "Video") {
            var type_two_res = type_two(creative)
            data['video_preview_image_url'] = type_two_res.video_preview_image_url
            data["video_url"] = type_two_res.video_url
            data["video_id"] = type_two_res.video_id
            data['type'] = 2
        } else {
            data['type'] = 1
            var type_one_res = type_one(__typename, __typename2, creative, content)
            data['image_url'] = type_one_res.image_url
            data['image_width'] = type_one_res.image_width
            data['image_height'] = type_one_res.image_height
            data['raw_cta_url'] = type_one_res.raw_cta_url
            data["title"] = type_one_res.title
            data["body"] = type_one_res.body
        }
        if (content["story"]["attachments"][0]["comet_footer_renderer"]) {
            var action_link = content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["action_links"][0]
            if (data['type'] !== 1) {
                data['raw_cta_url'] = action_link["url"]
                data['title'] = action_link["link_title"]
                data['body'] = action_link["link_description"]
                data['media'] = action_link["link_display"]
            }
        }
        data['comment_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]['comment_count']["total_count"];
        data['like_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]["reaction_count"]["count"]
        data['share_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]["share_count"]["count"]
        if (data['type'] === 2) {
            data['view_count'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']["comet_ufi_summary_and_actions_renderer"]["feedback"]["video_view_count"]
        }
        var _message = content["story"]["comet_sections"]["message"]
        data['message'] = _message == null ? null : _message["story"]["message"]["text"]
        if (content["story"]["attachments"][0]["comet_footer_renderer"] && content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["call_to_action_renderer"]) {
            var cta = content["story"]["attachments"][0]["comet_footer_renderer"]["attachment"]["call_to_action_renderer"]["action_link"]
            data['cta_text'] = cta["title"]
            data['cta_type'] = cta["link_type"]
        }
        var page = comet_sections["context_layout"]["story"]["comet_sections"]["actor_photo"]["story"]["actors"][0]
        data['page_id'] = page["id"]
        data['page_name'] = page["name"]
        data['page_profile_url'] = page["profile_url"]
        data['post_id'] = comet_sections['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']['subscription_target_id']
    }
    return data
}
function tryAnalysisPostdata(post_raw_data) {
    try {
        return analysisPostData(post_raw_data)
    } catch (error) {

        return null
    }
}
var sendMessageToBackground = (message, ads = []) => {
    chrome.runtime.sendMessage(extensionId, { message, ads })
}
var resultarr = []
var origOpen = XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open = function () {
    this.addEventListener('load', function () {
        try {
            var ads = this.responseText.split("\n");
            // console.log(ads, 'ads ads ads ads ads ads ads ads ads')
        } catch (e) { }
        try {
            ads.forEach(function (ad) {
                try {
                    ad = JSON.parse(ad);
                    if (ad.label) {
                        if (ad.label == "CometNewsFeed_viewer$stream$CometNewsFeed_viewer_news_feed" || typeof (ad["data"]["viewer"]["news_feed"]["edges"][0]["category"]) !== "undefined") {
                            if (ad.data.category == "SPONSORED" || ad["data"]["viewer"]["news_feed"]["edges"][0]["category"] == "SPONSORED") {
                                if (ad.data.category == "SPONSORED") {
                                    var resultingObj = {}
                                    //console.log('ad', ad)

                                    resultingObj['title'] = ad['data']['node']['comet_sections']['context_layout']['story']['comet_sections']['title']['story']['actors'][0]['name'] ? ad['data']['node']['comet_sections']['context_layout']['story']['comet_sections']['title']['story']['actors'][0]['name'] : ""

                                    //console.log('title', resultingObj['title'])

                                    let testTitle = ad.data.node.comet_sections.context_layout.story.comet_sections.title.story.actors[0].name
                                    //console.log(testTitle, 'testTitle testTitle testTitle')

                                    resultingObj['profileUrl'] = ad['data']['node']['comet_sections']['context_layout']['story']['comet_sections']['actor_photo']['story']['actors'][0]['profile_picture']['uri']

                                    //console.log('profileUrl', resultingObj['profileUrl'])

                                    resultingObj['description'] = ad['data']?.['node']['comet_sections']['content']['story']['comet_sections']['message']['story']['message']['text'] ? ad['data']['node']['comet_sections']['content']['story']['comet_sections']['message']['story']['message']['text'] : ""

                                    //console.log('description', resultingObj['description'])

                                    resultingObj['likesCount'] = ad['data']['node']['comet_sections']['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']['comet_ufi_summary_and_actions_renderer']
                                    ['feedback']['if_viewer_cannot_see_seen_by_member_list']['reaction_count']['count']

                                    //console.log('likesCount', resultingObj['likesCount'])

                                    // let tempctatext = ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['call_to_action_renderer']['action_link']['title']

                                    // console.log(tempctatext, 'tempctatext tempctatext')

                                    let ctatextt = ad?.data?.node?.comet_sections?.content?.story?.attachments[0]?.comet_footer_renderer?.attachment?.call_to_action_renderer?.action_link?.title

                                    //console.log(ctatextt, 'ctatextt ctatextt ctatextt ctatextt ctatextt ctatextt ctatextt ctatextt')

                                    resultingObj['ctaText'] = ctatextt ? ctatextt : ""
                                    // ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['call_to_action_renderer']['action_link']['title'] ?
                                    //     ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['call_to_action_renderer']['action_link']['title'] : ""

                                    //console.log('ctaText', resultingObj['ctaText'])



                                    // let tempCtaDomain = ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['source']['text'] ? ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['source']['text'] : ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['action_links']['destination_type']


                                    // resultingObj['ctaDomain'] = tempCtaDomain ? tempCtaDomain : "none"

                                    // console.log(resultingObj['ctaDomain'], 'tempCtaDomain tempCtaDomain tempCtaDomain')

                                    let tempCTADomain = ad?.data?.node?.comet_sections?.content?.story?.attachments[0]?.comet_footer_renderer?.attachment?.source?.text

                                    resultingObj['ctaDomain'] = tempCTADomain ? tempCTADomain : ""
                                    //console.log(resultingObj['ctaDomain'], 'ctaDomainn ctaDomainn ctaDomainn ctaDomainn ctaDomainn ctaDomainn')
                                    // resultingObj['ctaDomain'] = tempCtaDomain ? tempCtaDomain : ""


                                    // ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['source']['text'] ? ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['source']['text'] : ""

                                    // console.log('test test test', resultingObj['ctaDomain'])

                                    resultingObj['ctaDescription'] = ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['description']['text'] ? ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['description']['text'] : ""

                                    //console.log('ctaDescription', resultingObj['ctaDescription'])

                                    resultingObj['ctaHead'] = ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['styles']['attachment']['title_with_entities']['text'] ? ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['styles']['attachment']['title_with_entities']['text'] : "nothing in cta"

                                    //console.log('ctahead', resultingObj['ctahead'])

                                    resultingObj['sharecount'] = ad['data']['node']['comet_sections']['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']['comet_ufi_summary_and_actions_renderer']
                                    ['feedback']['share_count']['count'] ? ad['data']['node']['comet_sections']['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']['comet_ufi_summary_and_actions_renderer']
                                    ['feedback']['share_count']['count'] : 0

                                    //console.log('sharecount', resultingObj['sharecount'])

                                    resultingObj['commentsCount'] = ad['data']['node']['comet_sections']['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']['total_comment_count'] ? ad['data']['node']['comet_sections']['feedback']['story']['feedback_context']['feedback_target_with_context']['ufi_renderer']['feedback']['total_comment_count'] : 0

                                    //console.log('commentsCount', resultingObj['commentsCount'])

                                    resultingObj["adId"] = ad['data']['node']['post_id']

                                    //console.log('adId', resultingObj["adId"])

                                    resultingObj["pageId"] = ad['data']['node']['comet_sections']['context_layout']['story']['comet_sections']['actor_photo']['story']['actors'][0]['id'];

                                    //console.log('pageId', resultingObj["pageId"])

                                    resultingObj["redirectUrl"] = ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['call_to_action_renderer']['action_link']['url'] ? ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['comet_footer_renderer']['attachment']['call_to_action_renderer']['action_link']['url'] :
                                        ad['data']['node']['comet_sections']['content']['story']['actors'][0]['url']

                                    //console.log('redirectUrl', resultingObj["redirectUrl"])

                                    let tempVideoId = ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['styles']['attachment']['media']['videoId']
                                    if (tempVideoId != null) {
                                        resultingObj["videoId"] = tempVideoId
                                    }

                                    //console.log('tempVideoId', tempVideoId)
                                    resultarr.push(resultingObj)
                                } else { // data type of ad

                                    var resultingObj = {}
                                    resultingObj["adId"] = ad['data']['node']['post_id']
                                    resultingObj["pageId"] = ad['data']["viewer"]["news_feed"]["edges"][0]['node']['comet_sections']['context_layout']['story']['comet_sections']['actor_photo']['story']['actors'][0]['id'];
                                    resultingObj["title"] = ad['data']["viewer"]["news_feed"]["edges"][0]['node']['comet_sections']['context_layout']['story']['comet_sections']['title']['story']['actors'][0]['name'];
                                    resultingObj["redirectUrl"] = ad['data']["viewer"]["news_feed"]["edges"][0]['node']['comet_sections']['context_layout']['story']['comet_sections']['title']['story']['actors'][0]['url'];

                                    let tempVideoId = ad['data']['node']['comet_sections']['content']['story']['attachments'][0]['styles']['attachment']['media']['videoId']
                                    if (tempVideoId != null) {
                                        resultingObj["videoId"] = tempVideoId
                                    }
                                    resultarr.push(resultingObj)
                                }

                                // POST request using fetch()
                                sendMessageToBackground('post-facebook-ads', resultarr)
                                console.log(resultarr, 'resultarr')
                            }
                        }
                    }
                } catch (e) { }
            });
        } catch (e) { }
    });
    origOpen.apply(this, arguments);
};