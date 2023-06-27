/*******************
chrome_contextMenus_create-Handlebars_SafeString
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    new Handlebars.SafeString(n.linkUrl); // Expect 1 match here
    new Handlebars.SafeString(n.srcUrl); // Expect 1 match here
    new Handlebars.SafeString(n.pageUrl); // Expect 1 match here
    new Handlebars.SafeString(n.frameUrl); // Expect 1 match here
    new Handlebars.SafeString(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.srcUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.pageUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.frameUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.selectionText;
    new Handlebars.SafeString(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
new Handlebars.SafeString(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            new Handlebars.SafeString(v);
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
            new Handlebars.SafeString(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
new Handlebars.SafeString(x);

function aaa(n, a) {
    console.log();
    new Handlebars.SafeString(n.linkUrl); // Expect 1 match here
    new Handlebars.SafeString(n.srcUrl); // Expect 1 match here
    new Handlebars.SafeString(n.pageUrl); // Expect 1 match here
    new Handlebars.SafeString(n.frameUrl); // Expect 1 match here
    new Handlebars.SafeString(n.selectionText); // Expect 1 match here

    new Handlebars.SafeString(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.srcUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.pageUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.frameUrl;
    new Handlebars.SafeString(x); // Expect 1 match here

    x = n.selectionText;
    new Handlebars.SafeString(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            new Handlebars.SafeString(v);
        },
        onclick: function (n, a) {
            console.log();
            new Handlebars.SafeString(n.linkUrl); // Expect 1 match here
            new Handlebars.SafeString(n.srcUrl); // Expect 1 match here
            new Handlebars.SafeString(n.pageUrl); // Expect 1 match here
            new Handlebars.SafeString(n.frameUrl); // Expect 1 match here
            new Handlebars.SafeString(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.srcUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.pageUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.frameUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.selectionText;
            new Handlebars.SafeString(x); // Expect 1 match here
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
            new Handlebars.SafeString(v);
        },
        onclick: function kms(n, a) {
            console.log();
            new Handlebars.SafeString(n.linkUrl); // Expect 1 match here
            new Handlebars.SafeString(n.srcUrl); // Expect 1 match here
            new Handlebars.SafeString(n.pageUrl); // Expect 1 match here
            new Handlebars.SafeString(n.frameUrl); // Expect 1 match here
            new Handlebars.SafeString(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.srcUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.pageUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.frameUrl;
            new Handlebars.SafeString(x); // Expect 1 match here

            x = n.selectionText;
            new Handlebars.SafeString(x); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
