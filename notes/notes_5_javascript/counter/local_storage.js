// localStorage.getItem(key):
// This function searches for an entry in local storage with a given key, and returns the value associated with that key.

// localStorage.setItem(key, value): 
// This function sets and entry in local storage, associating the key with a new value.

// Checks if there is already a value in local storage
if (!localStorage.getItem("counter")) {
  // If not, sets the counter to 0 in local storage
  localStorage.setItem("counter", 0);
}

function count() {
  // Retrieves counter value from local storage
  let counter = localStorage.getItem("counter");

  // Updates the counter
  counter++;
  document.querySelector("h1").innerHTML = counter;

  // Stores counter in local storage
  localStorage.setItem("counter", counter);
}

document.addEventListener("DOMContentLoaded", function () {
  // Sets initial heading value to the current value inside local storage
  document.querySelector("h1").innerHTML = localStorage.getItem("counter");

  // Calls the 'count' function upon clicking the button
  document.querySelector("button").onclick = count;
});
