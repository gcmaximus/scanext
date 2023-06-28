// popup.js
document.addEventListener('DOMContentLoaded', function() {
  // Get the query parameter value from the URL
  var urlParams = new URLSearchParams(window.location.search);
  var queryParamValue = urlParams.get('param');

  // Display the query parameter value in the popup
  var queryParameterElement = document.getElementById('queryParameter');
  queryParameterElement.innerHTML = 'Query Parameter Value: ' + queryParamValue;
});
