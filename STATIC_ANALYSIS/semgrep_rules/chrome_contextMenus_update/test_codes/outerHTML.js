/*******************
chrome_contextMenus_update-outerHTML
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.srcUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.pageUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.frameUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.selectionText;
    document.getElementById("f").outerHTML = x; // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
document.getElementById("f").outerHTML = x;

chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").outerHTML = v;
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
            document.getElementById("f").outerHTML = v;
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
document.getElementById("f").outerHTML = x;

function aaa(n, a) {
    console.log();
    document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here

    document.getElementById("f").outerHTML = a.linkUrl;
    console.log();

    let x = n.linkUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.srcUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.pageUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.frameUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n.selectionText;
    document.getElementById("f").outerHTML = x; // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").outerHTML = v;
        },
        onclick: function (n, a) {
            console.log();
            document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.srcUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.pageUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.frameUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.selectionText;
            document.getElementById("f").outerHTML = x; // Expect 1 match here
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
            document.getElementById("f").outerHTML = v;
        },
        onclick: function bbb(n, a) {
            console.log();
            document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.srcUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.pageUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.frameUrl;
            document.getElementById("f").outerHTML = x; // Expect 1 match here

            x = n.selectionText;
            document.getElementById("f").outerHTML = x; // Expect 1 match here
            console.log();

            document.getElementById(x).outerHTML = "a";
        },
        test2: "sdfs",
    },
    "adfs"
);
