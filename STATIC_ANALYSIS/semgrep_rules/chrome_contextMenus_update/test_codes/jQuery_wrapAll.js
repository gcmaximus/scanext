/*******************
chrome_contextMenus_update-jQuery_wrapAll
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").wrapAll(n.linkUrl); // Expect 1 match here
    $("f").wrapAll(n.srcUrl); // Expect 1 match here
    $("f").wrapAll(n.pageUrl); // Expect 1 match here
    $("f").wrapAll(n.frameUrl); // Expect 1 match here
    $("f").wrapAll(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapAll(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").wrapAll(x);

chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapAll(v);
        },
        onclick: kms,
        test2: "sdfs",
    },
    "adfs"
);

// case 2
chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapAll(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").wrapAll(x);

function aaa(n, a) {
    console.log();
    $("f").wrapAll(n.linkUrl); // Expect 1 match here
    $("f").wrapAll(n.srcUrl); // Expect 1 match here
    $("f").wrapAll(n.pageUrl); // Expect 1 match here
    $("f").wrapAll(n.frameUrl); // Expect 1 match here
    $("f").wrapAll(n.selectionText); // Expect 1 match here

    $("f").wrapAll(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapAll(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapAll(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").wrapAll(n.linkUrl); // Expect 1 match here
            $("f").wrapAll(n.srcUrl); // Expect 1 match here
            $("f").wrapAll(n.pageUrl); // Expect 1 match here
            $("f").wrapAll(n.frameUrl); // Expect 1 match here
            $("f").wrapAll(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.selectionText;
            $("f").wrapAll(x); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);

// case 4
chrome.contextMenus.update(
    {
        ontest: function sss(n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapAll(v);
        },
        onclick: function bbb(n, a) {
            console.log();
            $("f").wrapAll(n.linkUrl); // Expect 1 match here
            $("f").wrapAll(n.srcUrl); // Expect 1 match here
            $("f").wrapAll(n.pageUrl); // Expect 1 match here
            $("f").wrapAll(n.frameUrl); // Expect 1 match here
            $("f").wrapAll(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").wrapAll(x); // Expect 1 match here

            x = n.selectionText;
            $("f").wrapAll(x); // Expect 1 match here
            console.log();

            $(x).wrapAll("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
