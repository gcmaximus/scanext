/*******************
chrome_contextMenus_create-eval
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    eval(n.linkUrl); // Expect 1 match here
    eval(n.srcUrl); // Expect 1 match here
    eval(n.pageUrl); // Expect 1 match here
    eval(n.frameUrl); // Expect 1 match here
    eval(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    eval(x); // Expect 1 match here

    x = n.srcUrl;
    eval(x); // Expect 1 match here

    x = n.pageUrl;
    eval(x); // Expect 1 match here

    x = n.frameUrl;
    eval(x); // Expect 1 match here

    x = n.selectionText;
    eval(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
eval(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            eval(v);
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
            eval(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
eval(x);

function aaa(n, a) {
    console.log();
    eval(n.linkUrl); // Expect 1 match here
    eval(n.srcUrl); // Expect 1 match here
    eval(n.pageUrl); // Expect 1 match here
    eval(n.frameUrl); // Expect 1 match here
    eval(n.selectionText); // Expect 1 match here

    eval(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    eval(x); // Expect 1 match here

    x = n.srcUrl;
    eval(x); // Expect 1 match here

    x = n.pageUrl;
    eval(x); // Expect 1 match here

    x = n.frameUrl;
    eval(x); // Expect 1 match here

    x = n.selectionText;
    eval(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            eval(v);
        },
        onclick: function (n, a) {
            console.log();
            eval(n.linkUrl); // Expect 1 match here
            eval(n.srcUrl); // Expect 1 match here
            eval(n.pageUrl); // Expect 1 match here
            eval(n.frameUrl); // Expect 1 match here
            eval(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            eval(x); // Expect 1 match here

            x = n.srcUrl;
            eval(x); // Expect 1 match here

            x = n.pageUrl;
            eval(x); // Expect 1 match here

            x = n.frameUrl;
            eval(x); // Expect 1 match here

            x = n.selectionText;
            eval(x); // Expect 1 match here
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
            eval(v);
        },
        onclick: function bbb(n, a) {
            console.log();
            eval(n.linkUrl); // Expect 1 match here
            eval(n.srcUrl); // Expect 1 match here
            eval(n.pageUrl); // Expect 1 match here
            eval(n.frameUrl); // Expect 1 match here
            eval(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            eval(x); // Expect 1 match here

            x = n.srcUrl;
            eval(x); // Expect 1 match here

            x = n.pageUrl;
            eval(x); // Expect 1 match here

            x = n.frameUrl;
            eval(x); // Expect 1 match here

            x = n.selectionText;
            eval(x); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
