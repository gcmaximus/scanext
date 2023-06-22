// Wrap the target element with a specific class based on the value in location.hash
function wrapElementBasedOnHash() {
    const targetElement = $('.target-element');
    const hashValue = location.hash.substring(1);
    var abc = location.hash
  
    // Wrap the target element with a specific class based on the hash value
    targetElement.wrap(`<div class="${hashValue}-wrapper"></div>`);
    targetElement.wrap(`<div class="${abc}-wrapper"></div>`);
    targetElement.wrap(`<div class="${location.hash}-wrapper"</div>`)
    targetElement.wrap(`<div class="location.hash-wrapper"</div>`)
    $(hashValue).wrap(`<div>CAONIMA</div>`)
  }
  
  // Call the function when the hash changes or on initial page load
  $(document).ready(function() {
    wrapElementBasedOnHash();
  });
  
  $(window).on('hashchange', function() {
    wrapElementBasedOnHash();
  });
  