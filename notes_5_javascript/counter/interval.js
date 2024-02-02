let counter = 0;

function count() {
  counter++;
  document.querySelector("h1").innerHTML = counter;
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("button").onclick = count;

  // the 'setInterval' function takes an argument as a function to be run, and a time (in milliseconds) between function runs.
  // https://developer.mozilla.org/en-US/docs/Web/API/setInterval
  setInterval(count, 1000);
});
