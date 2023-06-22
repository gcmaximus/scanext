// Update bookmark details based on the value in location.hash
function updateBookmarkDetailsBasedOnHash() {
  const targetElement = document.getElementById('bookmark-details');
  const bookmarkId = location.hash.substring(1);

  // Simulated data for bookmark details
  const bookmarkDetails = {
    id: bookmarkId,
    title: 'Example Bookmark',
    url: 'https://www.example.com',
    description: 'This is an example bookmark',
    tags: ['tag1', 'tag2', 'tag3']
  };

  // Update the target element's content using innerHTML
  targetElement.innerHTML = `
    <h1>ID: ${bookmarkDetails.bookmarkId}
    <h2>${bookmarkDetails.title}</h2>
    <p>Description: ${bookmarkDetails.description}</p>
    <p>URL: <a href="${bookmarkDetails.url}" target="_blank">${bookmarkDetails.url}</a></p>
    <p>Tags: ${bookmarkDetails.tags.join(', ')}</p>
  `;

  bookmarkId.innerHTML = 'abc'
  
  $('.testing').innerHTML = "this is ID: bookmarkId"
  $('.marker').innerHTML = "this is ID: " + bookmarkId
  
}

// Call the function when the hash changes or on initial page load
window.addEventListener('DOMContentLoaded', updateBookmarkDetailsBasedOnHash);
window.addEventListener('hashchange', updateBookmarkDetailsBasedOnHash);
