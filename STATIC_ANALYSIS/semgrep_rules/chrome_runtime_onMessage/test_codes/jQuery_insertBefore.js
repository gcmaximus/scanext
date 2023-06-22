//LINES 2-11 is an example of inserting a custom icon before specific links
chrome.runtime.onMessage.addListener(({ action, iconUrl, targetUrls }) => {
    if (action === 'insertIconBeforeLinks') {
      $('a').each((_, element) => {
        const href = $(element).attr('href');
        if (targetUrls.includes(href)) {
          $(`<img src="${iconUrl}" class="custom-icon">`).insertBefore(element);
        }
      });
    }
  });
  //LINES 13-21 is an example of wrapping image elements with a custom container
  chrome.runtime.onMessage.addListener(({ action, containerClass }) => {
    if (action === 'wrapImagesWithContainer') {
      $('img').each((_, element) => {
        const $image = $(element);
        const $container = $('<div>').addClass(containerClass);
        $image.insertBefore($container);
      });
    }
  });
  //LINES 23-30 is an example of inserting a loading spinner before specific elements
  chrome.runtime.onMessage.addListener(({ action, targetClass }) => {
    if (action === 'insertLoadingSpinner') {
      $(`.${targetClass}`).each((_, element) => {
        const $spinner = $('<div>').addClass('loading-spinner');
        $spinner.insertBefore(element);
      });
    }
  });
  //LINES 32-39 is an example of prepending a timestamp before each comment
  chrome.runtime.onMessage.addListener(({ action }) => {
    if (action === 'prependTimestampToComments') {
      $('.comment').each((_, element) => {
        const timestamp = new Date().toLocaleString();
        $(`<span class="comment-timestamp">${timestamp}</span>`).insertBefore(element);
      });
    }
  });
  // 4 matches to be found