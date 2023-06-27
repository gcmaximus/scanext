/*******************
chrome_contextMenus_create-jQuery_prependTo
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$(x).prependTo("f");

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").prependTo(v);
        },
        onclick: kms,
        test2: "sdfs",
    },
    "adfs"
);

// case 2
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").prependTo(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$(x).prependTo("f");

function aaa(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here

    $("f").prependTo(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").prependTo(v);
        },
        onclick: function (n, a) {
            console.log();
            $(n.linkUrl).prependTo("f"); // Expect 1 match here
            $(n.srcUrl).prependTo("f"); // Expect 1 match here
            $(n.pageUrl).prependTo("f"); // Expect 1 match here
            $(n.frameUrl).prependTo("f"); // Expect 1 match here
            $(n.selectionText).prependTo("f"); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.srcUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.pageUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.frameUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.selectionText;
            $(x).prependTo("f"); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);

// case 4
chrome.contextMenus.create(
    {
        ontest: function sss(n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").prependTo(v);
        },
        onclick: function bbb(n, a) {
            console.log();
            $(n.linkUrl).prependTo("f"); // Expect 1 match here
            $(n.srcUrl).prependTo("f"); // Expect 1 match here
            $(n.pageUrl).prependTo("f"); // Expect 1 match here
            $(n.frameUrl).prependTo("f"); // Expect 1 match here
            $(n.selectionText).prependTo("f"); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.srcUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.pageUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.frameUrl;
            $(x).prependTo("f"); // Expect 1 match here

            x = n.selectionText;
            $(x).prependTo("f"); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
