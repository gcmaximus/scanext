//LINES 2-8 is an example of inserting a custom element before each image element
chrome.runtime.onMessage.addListener(({ action, element }) => {
    if (action === 'insertCustomElementBeforeImages') {
      $('img').each((_, element) => {
        $(element).before($(element));
      });
    }
  });
  //LINES 10-16 is an example of injecting a number span before each paragraph element
  chrome.runtime.onMessage.addListener(({ action }) => {
    if (action === 'numberParagraphs') {
      $('p').each((index, element) => {
        $(element).before(`<span class="paragraph-number">${index + 1}</span>`);
      });
    }
  });
  //LINES 18-24 is an example of adding a prefix to each heading element
  chrome.runtime.onMessage.addListener(({ action }) => {
    if (action === 'numberParagraphs') {
      $('p').each((index, element) => {
        $(element).before(`<span class="paragraph-number">${index + 1}</span>`);
      });
    }
  });
  //LINES 26-33 is an example of inserting a loading spinner before specific elements
  chrome.runtime.onMessage.addListener(({ action, targetClass }) => {
    if (action === 'insertLoadingSpinner') {
      $(`.${targetClass}`).each((_, element) => {
        const $spinner = $('<div>').addClass('loading-spinner');
        $(element).before($spinner);
      });
    }
  });
  //LINES 35-42 is an example of prepending a timestamp before each comment
  chrome.runtime.onMessage.addListener(({ action }) => {
    if (action === 'prependTimestampToComments') {
      $('.comment').each((_, element) => {
        const timestamp = new Date().toLocaleString();
        $(element).before(`<span class="comment-timestamp">${timestamp}</span>`);
      });
    }
  });
  