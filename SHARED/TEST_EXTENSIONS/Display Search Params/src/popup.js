function toDo(tab) {
  //location.search
  query = window.location.search

  // Find the element on the webpage where you want to display the search parameter
  const elements = document.getElementsByTagName('h1');

  // Set the innerHTML of the element to the search parameter value
  for (let i = 0; i < elements.length; i++) {
    var query = decodeURI(query)
    console.log(query)
    elements[i].innerHTML = `Your query is: ${query}`
  }
}
async function getCurrentTab() {
  let queryOptions = { active: true, currentWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  // console.log(tab)
  return tab;
}

getCurrentTab().then((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: toDo,
    args: [tab],
  });
});