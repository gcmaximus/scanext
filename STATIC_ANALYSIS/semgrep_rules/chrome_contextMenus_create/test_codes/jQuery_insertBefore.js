/*******************
chrome_contextMenus_create-jQuery_insertBefore
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).insertBefore("f"); // Expect 1 match here
    $(n.srcUrl).insertBefore("f"); // Expect 1 match here
    $(n.pageUrl).insertBefore("f"); // Expect 1 match here
    $(n.frameUrl).insertBefore("f"); // Expect 1 match here
    $(n.selectionText).insertBefore("f"); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$(x).insertBefore("f");

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertBefore(v);
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
            $("f").insertBefore(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$(x).insertBefore("f");

function aaa(n, a) {
    console.log();
    $(n.linkUrl).insertBefore("f"); // Expect 1 match here
    $(n.srcUrl).insertBefore("f"); // Expect 1 match here
    $(n.pageUrl).insertBefore("f"); // Expect 1 match here
    $(n.frameUrl).insertBefore("f"); // Expect 1 match here
    $(n.selectionText).insertBefore("f"); // Expect 1 match here

    $("f").insertBefore(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertBefore(v);
        },
        onclick: function (n, a) {
            console.log();
            $(n.linkUrl).insertBefore("f"); // Expect 1 match here
            $(n.srcUrl).insertBefore("f"); // Expect 1 match here
            $(n.pageUrl).insertBefore("f"); // Expect 1 match here
            $(n.frameUrl).insertBefore("f"); // Expect 1 match here
            $(n.selectionText).insertBefore("f"); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.srcUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.pageUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.frameUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.selectionText;
            $(x).insertBefore("f"); // Expect 1 match here
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
            $("f").insertBefore(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $(n.linkUrl).insertBefore("f"); // Expect 1 match here
            $(n.srcUrl).insertBefore("f"); // Expect 1 match here
            $(n.pageUrl).insertBefore("f"); // Expect 1 match here
            $(n.frameUrl).insertBefore("f"); // Expect 1 match here
            $(n.selectionText).insertBefore("f"); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.srcUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.pageUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.frameUrl;
            $(x).insertBefore("f"); // Expect 1 match here

            x = n.selectionText;
            $(x).insertBefore("f"); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
