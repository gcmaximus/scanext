/*******************
chrome_contextMenus_create-jQuery_insertAfter
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).insertAfter('f'); // Expect 1 match here
    $(n.srcUrl).insertAfter('f'); // Expect 1 match here
    $(n.pageUrl).insertAfter('f'); // Expect 1 match here
    $(n.frameUrl).insertAfter('f'); // Expect 1 match here
    $(n.selectionText).insertAfter('f'); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.selectionText;
    $(x).insertAfter('f'); // Expect 1 match here
    console.log();
}

let a = n.linkUrl;
$(x).insertAfter('f');

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertAfter(v);
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
            $("f").insertAfter(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$(x).insertAfter('f');

function aaa(n, a) {
    console.log();
    $(n.linkUrl).insertAfter('f'); // Expect 1 match here
    $(n.srcUrl).insertAfter('f'); // Expect 1 match here
    $(n.pageUrl).insertAfter('f'); // Expect 1 match here
    $(n.frameUrl).insertAfter('f'); // Expect 1 match here
    $(n.selectionText).insertAfter('f'); // Expect 1 match here

    $("f").insertAfter(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertAfter('f'); // Expect 1 match here

    x = n.selectionText;
    $(x).insertAfter('f'); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertAfter(v);
        },
        onclick: function (n, a) {
            console.log();
            $(n.linkUrl).insertAfter('f'); // Expect 1 match here
            $(n.srcUrl).insertAfter('f'); // Expect 1 match here
            $(n.pageUrl).insertAfter('f'); // Expect 1 match here
            $(n.frameUrl).insertAfter('f'); // Expect 1 match here
            $(n.selectionText).insertAfter('f'); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.srcUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.pageUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.frameUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.selectionText;
            $(x).insertAfter('f'); // Expect 1 match here
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
            $("f").insertAfter(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $(n.linkUrl).insertAfter('f'); // Expect 1 match here
            $(n.srcUrl).insertAfter('f'); // Expect 1 match here
            $(n.pageUrl).insertAfter('f'); // Expect 1 match here
            $(n.frameUrl).insertAfter('f'); // Expect 1 match here
            $(n.selectionText).insertAfter('f'); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.srcUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.pageUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.frameUrl;
            $(x).insertAfter('f'); // Expect 1 match here

            x = n.selectionText;
            $(x).insertAfter('f'); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
