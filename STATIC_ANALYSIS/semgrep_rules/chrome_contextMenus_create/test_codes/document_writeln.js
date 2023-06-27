/*******************
chrome_contextMenus_create-document_write
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    document.writeln(n.linkUrl); // Expect 1 match here
    document.writeln(n.srcUrl); // Expect 1 match here
    document.writeln(n.pageUrl); // Expect 1 match here
    document.writeln(n.frameUrl); // Expect 1 match here
    document.writeln(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    document.writeln(x); // Expect 1 match here

    x = n.srcUrl;
    document.writeln(x); // Expect 1 match here

    x = n.pageUrl;
    document.writeln(x); // Expect 1 match here

    x = n.frameUrl;
    document.writeln(x); // Expect 1 match here

    x = n.selectionText;
    document.writeln(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
document.writeln(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.writeln(v);
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
            document.writeln(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
document.writeln(x);

function aaa(n, a) {
    console.log();
    document.writeln(n.linkUrl); // Expect 1 match here
    document.writeln(n.srcUrl); // Expect 1 match here
    document.writeln(n.pageUrl); // Expect 1 match here
    document.writeln(n.frameUrl); // Expect 1 match here
    document.writeln(n.selectionText); // Expect 1 match here

    document.writeln(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    document.writeln(x); // Expect 1 match here

    x = n.srcUrl;
    document.writeln(x); // Expect 1 match here

    x = n.pageUrl;
    document.writeln(x); // Expect 1 match here

    x = n.frameUrl;
    document.writeln(x); // Expect 1 match here

    x = n.selectionText;
    document.writeln(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.writeln(v);
        },
        onclick: function (n, a) {
            console.log();
            document.writeln(n.linkUrl); // Expect 1 match here
            document.writeln(n.srcUrl); // Expect 1 match here
            document.writeln(n.pageUrl); // Expect 1 match here
            document.writeln(n.frameUrl); // Expect 1 match here
            document.writeln(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            document.writeln(x); // Expect 1 match here

            x = n.srcUrl;
            document.writeln(x); // Expect 1 match here

            x = n.pageUrl;
            document.writeln(x); // Expect 1 match here

            x = n.frameUrl;
            document.writeln(x); // Expect 1 match here

            x = n.selectionText;
            document.writeln(x); // Expect 1 match here
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
            document.writeln(v);
        },
        onclick: function kms(n, a) {
            console.log();
            document.writeln(n.linkUrl); // Expect 1 match here
            document.writeln(n.srcUrl); // Expect 1 match here
            document.writeln(n.pageUrl); // Expect 1 match here
            document.writeln(n.frameUrl); // Expect 1 match here
            document.writeln(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            document.writeln(x); // Expect 1 match here

            x = n.srcUrl;
            document.writeln(x); // Expect 1 match here

            x = n.pageUrl;
            document.writeln(x); // Expect 1 match here

            x = n.frameUrl;
            document.writeln(x); // Expect 1 match here

            x = n.selectionText;
            document.writeln(x); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
