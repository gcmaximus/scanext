/*******************
chrome_contextMenus_create-jQuery_before
*******************/


// Expected total matches: 40


// case 1
function kms(n, a) {
    console.log();
    $("f").before(n.linkUrl); // Expect 1 match here
    $("f").before(n.srcUrl); // Expect 1 match here
    $("f").before(n.pageUrl); // Expect 1 match here
    $("f").before(n.frameUrl); // Expect 1 match here
    $("f").before(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl; 
    $("f").before(x); // Expect 1 match here
    
    x = n.srcUrl;
    $("f").before(x); // Expect 1 match here
    
    x = n.pageUrl;
    $("f").before(x); // Expect 1 match here
    
    x = n.frameUrl;
    $("f").before(x); // Expect 1 match here
    
    x = n.selectionText;
    $("f").before(x); // Expect 1 match here
    console.log();
}

let a = n.linkUrl;
$("f").before(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").before(v);
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
            $("f").before(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").before(x);

function aaa(n, a) {
    console.log();
    $("f").before(n.linkUrl); // Expect 1 match here
    $("f").before(n.srcUrl); // Expect 1 match here
    $("f").before(n.pageUrl); // Expect 1 match here
    $("f").before(n.frameUrl); // Expect 1 match here
    $("f").before(n.selectionText); // Expect 1 match here

    $("f").before(a.linkUrl);
    console.log();

    let x = n.linkUrl; 
    $("f").before(x); // Expect 1 match here
    
    x = n.srcUrl;
    $("f").before(x); // Expect 1 match here
    
    x = n.pageUrl;
    $("f").before(x); // Expect 1 match here
    
    x = n.frameUrl;
    $("f").before(x); // Expect 1 match here
    
    x = n.selectionText;
    $("f").before(x); // Expect 1 match here
    console.log();
}


// case 3
chrome.contextMenus.create(
    {
        ontest: function(n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").before(v);
        },
        onclick: function(n, a) {
            console.log();
            $("f").before(n.linkUrl); // Expect 1 match here
            $("f").before(n.srcUrl); // Expect 1 match here
            $("f").before(n.pageUrl); // Expect 1 match here
            $("f").before(n.frameUrl); // Expect 1 match here
            $("f").before(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl; 
            $("f").before(x); // Expect 1 match here
            
            x = n.srcUrl;
            $("f").before(x); // Expect 1 match here
            
            x = n.pageUrl;
            $("f").before(x); // Expect 1 match here
            
            x = n.frameUrl;
            $("f").before(x); // Expect 1 match here
            
            x = n.selectionText;
            $("f").before(x); // Expect 1 match here
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
            $("f").before(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").before(n.linkUrl); // Expect 1 match here
            $("f").before(n.srcUrl); // Expect 1 match here
            $("f").before(n.pageUrl); // Expect 1 match here
            $("f").before(n.frameUrl); // Expect 1 match here
            $("f").before(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl; 
            $("f").before(x); // Expect 1 match here
            
            x = n.srcUrl;
            $("f").before(x); // Expect 1 match here
            
            x = n.pageUrl;
            $("f").before(x); // Expect 1 match here
            
            x = n.frameUrl;
            $("f").before(x); // Expect 1 match here
            
            x = n.selectionText;
            $("f").before(x); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
