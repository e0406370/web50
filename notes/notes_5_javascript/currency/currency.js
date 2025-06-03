document.addEventListener("DOMContentLoaded", function () {

  document.querySelector("form").onsubmit = function () {

    // Sends a GET request to the URL
    fetch("https://api.exchangeratesapi.io/latest?base=USD")
    
      // Puts response into json form
      .then((response) => response.json())

      .then((data) => {

        // Gets currency from user input and convert to upper case
        const currency = document
          .querySelector("#currency")
          .value.toUpperCase();

        // Gets rate from data
        const rate = data.rates[currency];

        // Checks if currency is valid:
        if (rate !== undefined) {

          // Displays exchange on the screen
          document.querySelector("#result").innerHTML = `1 USD is equal to ${rate.toFixed(3)} ${currency}.`;
        }
        else {

          // Displays error on the screen
          document.querySelector("#result").innerHTML = "Invalid Currency.";
        }
      })

      // Catches any errors and log them to the console
      .catch((error) => {
        console.log("Error:", error);
      });
    
    // Prevents default submission
    return false;
  };
});