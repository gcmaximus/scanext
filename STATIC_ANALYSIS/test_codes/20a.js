/*******************
20a. chrome.contextMenus.create  
*******************/

// Expected total match: 30

// case 1
function kms(n, a) {
    console.log();
    document.getElementById("f").innerHTML = n.linkUrl;
    document.getElementById("f").innerHTML = n.srcUrl;
    document.getElementById("f").innerHTML = n.pageUrl;
    document.getElementById("f").innerHTML = n.frameUrl;
    document.getElementById("f").innerHTML = n.selectionText;

    console.log();

    let x = n.linkUrl;
    document.getElementById("f").innerHTML = x;
    x = n.srcUrl;
    document.getElementById("f").innerHTML = x;
    x = n.pageUrl;
    document.getElementById("f").innerHTML = x;
    x = n.frameUrl;
    document.getElementById("f").innerHTML = x;
    x = n.selectionText;
    document.getElementById("f").innerHTML = x;
    console.log();
}

let a = n.linkUrl;
document.getElementById("f").innerHTML = x;

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").innerHTML = v;
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
            document.getElementById("f").innerHTML = v;
        },
        onclick: kms,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
document.getElementById("f").innerHTML = x;

function kms(n, a) {
    console.log();
    document.getElementById("f").innerHTML = n.linkUrl;
    document.getElementById("f").innerHTML = n.srcUrl;
    document.getElementById("f").innerHTML = n.pageUrl;
    document.getElementById("f").innerHTML = n.frameUrl;
    document.getElementById("f").innerHTML = n.selectionText;

    console.log();

    let x = n.linkUrl;
    document.getElementById("f").innerHTML = x;
    x = n.srcUrl;
    document.getElementById("f").innerHTML = x;
    x = n.pageUrl;
    document.getElementById("f").innerHTML = x;
    x = n.frameUrl;
    document.getElementById("f").innerHTML = x;
    x = n.selectionText;
    document.getElementById("f").innerHTML = x;
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").innerHTML = v;
        },
        onclick: function (n, a) {
            console.log();
            document.getElementById("f").innerHTML = n.linkUrl;
            document.getElementById("f").innerHTML = n.srcUrl;
            document.getElementById("f").innerHTML = n.pageUrl;
            document.getElementById("f").innerHTML = n.frameUrl;
            document.getElementById("f").innerHTML = n.selectionText;
            console.log();

            let x = n.linkUrl;
            document.getElementById("f").innerHTML = x;
            x = n.srcUrl;
            document.getElementById("f").innerHTML = x;
            x = n.pageUrl;
            document.getElementById("f").innerHTML = x;
            x = n.frameUrl;
            document.getElementById("f").innerHTML = x;
            x = n.selectionText;
            document.getElementById("f").innerHTML = x;
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
            document.getElementById("f").innerHTML = v;
        },
        onclick: function kms(n, a) {
            console.log();
            document.getElementById("f").innerHTML = n.linkUrl;
            document.getElementById("f").innerHTML = n.srcUrl;
            document.getElementById("f").innerHTML = n.pageUrl;
            document.getElementById("f").innerHTML = n.frameUrl;
            document.getElementById("f").innerHTML = n.selectionText;
            console.log();

            let x = n.linkUrl;
            document.getElementById("f").innerHTML = x;
            x = n.srcUrl;
            document.getElementById("f").innerHTML = x;
            x = n.pageUrl;
            document.getElementById("f").innerHTML = x;
            x = n.frameUrl;
            document.getElementById("f").innerHTML = x;
            x = n.selectionText;
            document.getElementById("f").innerHTML = x;
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
