
chrome.storage.sync.get(['catdata'], (data) => {
    if (!Object.keys(data).length) {
        return createCatdata();
    }
    else {
        updateSettings(data.catdata.settings);
        updateTotal(data.catdata.stats.total);
        updateCats(data.catdata.stats.cats);
        primeBlockedSites(data.catdata.settings.blocked_sites);
    }
});

document.addEventListener('DOMContentLoaded', function() {

    primeCheckboxes();
    primeBlockedSitesButton();
    primeBlockNewSiteButton();
    askActiveTabForUrl();

    function primeCheckboxes() {
        primeOnOff();
        primeVolume();
        primeAllCheckboxes();
    }

    function primeAllCheckboxes() {
        let checkboxes = [...document.getElementsByTagName('checkbox')];
        for (let i = 0; i < checkboxes.length; i++) {
            checkboxes[i].addEventListener('click', toggleChecked);
            function toggleChecked() {
                checkboxes[i].className = checkboxes[i].className === 'checked' ? 'unchecked' : 'checked';
            }
        }
    }

    function primeOnOff() {
        document.getElementById('on').addEventListener('click', toggleOnOff);
        function toggleOnOff() {
            let onText = document.getElementById('on-off');
            onText.innerText = onText.innerText === 'On' ? 'Off' : 'On';
            onText.innerText === 'Off' && removeAllCatButtons();
        }
        function removeAllCatButtons() {
            chrome.tabs.query({}, sendMessages);
            function sendMessages (tabs) {
                tabs.forEach( (tab) => { 
                    chrome.tabs.sendMessage(tab.id, {title:'OFF'}); 
                } );
            }
        }
    }

    function primeVolume() {
        let volumeBtn = document.getElementById('volume');
        volumeBtn.addEventListener('click', muteMeow);

        function muteMeow() {
            if (volumeBtn.className === 'checked') {
                sendMessageToTab({title: 'MUTE'});
            }
        }
    }

    function primeBlockedSitesButton() {
        let btn = document.getElementById('blocked-btn');
        btn.addEventListener('click', showBlockedSites);
        function showBlockedSites() {
            let blockedBox = document.getElementById('site-blocker');
            blockedBox.className ? blockedBox.className = '' : blockedBox.className = 'invisible';
        }
    }

    function primeBlockNewSiteButton() {
        let btn = document.getElementById('block-site-btn');
        btn.addEventListener('click', blockSite);
        function blockSite() {
            let siteRaw = document.getElementById('block-site-input').value;
            let site = simplifyUrl(siteRaw);
            chrome.storage.sync.get(['catdata'], (data) => {

                let index = data.catdata.settings.blocked_sites.push(site) - 1;
                chrome.storage.sync.set(data);

                addBlockedSiteDiv(site, index);
            });
            document.getElementById('block-site-input').value = '';
        }
    }

    function askActiveTabForUrl() {
        sendMessageToTab({
            'title': 'SEND_URL'
        });
    }

}, {once : true});

function alertFailedConnection() {
    document.getElementById('cata-data').innerText = "Uh Oh, Poor Connection\n" +
    "we couldn't connect to the catabase";
}

function sendMessageToTab(message) {
    let tabParameters = {
        active: true,
        currentWindow: true
    };
    chrome.tabs.query(tabParameters, onGotTabs);

    function onGotTabs(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, message);
    }
}

chrome.runtime.onMessage.addListener(receivedMessage);

function receivedMessage(message, sender, sendResponse) {
  switch (message.title) {
    case "URL" : 
        processActiveTabUrl(message.url);
        break;
  }
}

function primeBlockedSites(blockedSites) {
    for (let i = 0; i < blockedSites.length; i++) {
        addBlockedSiteDiv(blockedSites[i], i);
    }
}
  
function addBlockedSiteDiv(blockedSite, index) {

    let box = document.createElement('div');
    box.id = 'blocked-' + index;
    let sitetext = document.createElement('sitetext');
    sitetext.innerText = blockedSite;
    let unblockBtn = createUnblockBtn(index);
    box.append(sitetext);
    box.append(unblockBtn);
    document.getElementById('site-blocker').append(box);

    unblockBtn.addEventListener('click', unblock);
    function unblock() {
        chrome.storage.sync.get(['catdata'], (data) => {
            data.catdata.settings.blocked_sites.splice(index, 1);
            chrome.storage.sync.set(data);
        });
        box.remove();
    }
}

function createUnblockBtn(id) {
    let unblockBtn = document.createElement('button');
    unblockBtn.className = 'unblock btn-sm';
    unblockBtn.innerText = 'unblock';
    unblockBtn.id = 'unblock-' + id;
    return unblockBtn;
}

function processActiveTabUrl(url) {
    chrome.storage.sync.get(['catdata'], (data) => {
        if (!data.catdata.settings.blocked_sites.includes(url)) {
            setCurrentTabUrl(url);
        } else {
            setFirstBlockedSite(url, data.catdata.settings.blocked_sites);
            createBlockedOnSiteNotification(url);
        }
    });
}

function setCurrentTabUrl(url) {
    document.getElementById('block-site-input').value = url;
}

function setFirstBlockedSite(url, blockedSites) {
    let index = blockedSites.indexOf(url);
    document.getElementById('block-site-btn').after(document.getElementById('blocked-' + index));
}

function createBlockedOnSiteNotification(url) {
    let notif = document.createElement('button');
    notif.className = 'btn-sm';
    notif.style = 'display: block; float: right; margin-right: 10px; margin-bottom: 6px;';
    notif.innerText = 'Blocked on this site ' + url;
    notif.addEventListener('click', openBlockedBox);
    [...document.getElementsByTagName('header')][0].append(notif);

    function openBlockedBox() {
        document.getElementById('blocked-btn').click();
    }
}

function openMysmPage() {
    const url='https://chrome.google.com/webstore/detail/meow-you-see-me/ihkongdgoakeofnnepndjmffbpcghgei';
    window.open(url, '_blank');
}

function createCatdata() {
    let settings = { 
        'volume': false, 
        'on': true, 
        'blocked_sites': [] 
    };
    let stats = {
        'total': 0, 
        'cats': [] 
    };
    let catdata = { 
        'settings': settings, 
        'stats': stats
    }
    chrome.storage.sync.set({'catdata': catdata});
}

function updateSettings(settings) {
    updateVolume(settings.volume);
    updateOn(settings.on);
}

function updateVolume(volume) {
    let btn = document.getElementById('volume');
    if (volume) {
        btn.className = 'checked';
    }
    btn.addEventListener('click', toggleVolume);
    function toggleVolume() {
        chrome.storage.sync.get(['catdata'], (data) => {
            data.catdata.settings.volume = !data.catdata.settings.volume;
            chrome.storage.sync.set(data);
        });
    }
}

function updateOn(on) {
    let btn = document.getElementById('on');
    if (on) {
        btn.className = 'checked';
    } else {
        document.getElementById('on-off').innerText = 'Off';
    }
    btn.addEventListener('click', toggleOn);
    function toggleOn() {
        chrome.storage.sync.get(['catdata'], (data) => {
            data.catdata.settings.on = !data.catdata.settings.on;
            chrome.storage.sync.set(data);
        });
    }
}

function updateTotal(total) {
    document.getElementById('total').innerText = total;
}

function updateCats(cats) {
    cats = checkForDuplicateCats(cats);
    if (cats.length) {
        getCats();
    } else {
        noCatsYetMessage();
    }
    function getCats() {
        let ratio = cats.length === jsonCatData.cats.length ? 'All' : cats.length + '/' + jsonCatData.cats.length;
        addCollectedCatsHeader(ratio);
        for (let i = 0; i < cats.length; i++) {
            addCatProfile(findCat(jsonCatData.cats, cats[i]))
        }
        
    }
    function noCatsYetMessage() {
        document.getElementById('cata-data').innerText = 'No special cats collected yet';
    }
}

function checkForDuplicateCats(cats) {
    // make sure no duplicate cats exist
    let len = cats.length;
    for (let i = 0; i < cats.length; i++) {
        for (let j = i + 1; j < cats.length; j++) {
            while (cats[i] == cats[j]) {
                cats.splice(j, 1);
            }
        }
        let found = false;
        while (!found && i < cats.length) {
            for (let j = 0; j < jsonCatData.cats.length && !found; j++) {
                if (cats[i] == jsonCatData.cats[j].name) {
                    found = true;
                }
            }
            if (!found)
                cats.splice(i, 1);
        }
    }
    // if change occured
    if (len != cats.length) {
        // update cat data
        chrome.storage.sync.get(['catdata'], (data) => {
            data.catdata.stats.cats = cats;
            chrome.storage.sync.set(data);
        });
    }
    return cats;
}

function findCat(cats, catName) {
    for (let i = 0; i < cats.length; i++) {
        if (cats[i].name === catName) {
            return cats[i];
        }
    }
}

function addCollectedCatsHeader(ratio) {
    let collectedCatsHeader = document.getElementById('cata-data');
    collectedCatsHeader.innerText = ratio + ' Special Cats Collected';
}

function addCatProfile(cat) {
    if (!cat) {
        return;
    }
    let catProfile = document.createElement('catprofile');
    catProfile.innerText = cat.name;
    addRearrangeFunctionality(catProfile);
    let img = document.createElement('img');
    img.setAttribute('src', "data:image/png;base64," + cat.data);
    img.className='special-cat-img';
    catProfile.prepend(img);
    document.getElementById('litter-box').append(catProfile);
    if (cat.special_card) {
        specialCard(cat, catProfile)
    }
}

var draggedProfile = null;
function addRearrangeFunctionality(catProfile) {

    catProfile.setAttribute('draggable', true);

    catProfile.addEventListener('dragenter', catDragEnter, false);
    catProfile.addEventListener('dragstart', catDragStart, false);
    catProfile.addEventListener('dragend', catDragEnd, false);

    function catDragStart() {
        draggedProfile = catProfile;
    }

    function catDragEnter() {
        if (!draggedProfile) {
            return;
        }

        let profiles = [...document.getElementsByTagName('catprofile')];
        if (profiles.indexOf(draggedProfile) < profiles.indexOf(catProfile)) {
            catProfile.after(draggedProfile);
        } else {
            catProfile.before(draggedProfile);
        }
    }

    function catDragEnd() {
        if (!draggedProfile) {
            return;
        }

        saveArrangement();
        setTimeout(setDraggedNull, 0.05);

        function setDraggedNull() {
            draggedProfile = null;
        }
        function saveArrangement() {
            let profiles = [...document.getElementsByTagName('catprofile')];
            let cats = [];
            for (let i = 0; i < profiles.length; i++) {
                cats.push(profiles[i].innerText);
            }
            chrome.storage.sync.get(['catdata'], (data) => {
                data.catdata.stats.cats = cats;
                chrome.storage.sync.set(data);
            });
        }

    }
}

function simplifyUrl(url) {
  
    let ignoreStarts = ['https://', 'http://', 'www.'];
    for (let i = 0; i < ignoreStarts.length; i++) {
      let ignoreStart = ignoreStarts[i];
      if (url.includes(ignoreStart)) {
        url = url.substr(url.indexOf(ignoreStart) + ignoreStart.length);
      }
    }
  
    let ignoreEnds = ['/', '?', '#', '&'];
    for (let i = 0; i < ignoreEnds.length; i++) {
      let ignoreEnd = ignoreEnds[i];
      if (url.includes(ignoreEnd)) {
        url = url.substr(0, url.indexOf(ignoreEnd));
      }
    }
    url = url.toLowerCase();
    
    return url;
}