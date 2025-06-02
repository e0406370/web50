document.addEventListener("DOMContentLoaded", function () {

  // We use the querySelectorAll function to get a Node List
  // (similar to a Python list or a JavaScript array) with all elements that match the query.
  
  // The forEach function in JavaScript takes in another function, and applies that function to each element in a list or array.
  document.querySelectorAll("button").forEach(function (button) {

    button.onclick = function () {
      
      // We change the style of an element using the style.SOMETHING attribute.
      document.querySelector("#hello").style.color = button.dataset.color;
    };
    
  });

});

// Alternative Notation : Arrow Function

// document.addEventListener('DOMContentLoaded', () => {

//   document.querySelectorAll('button').forEach(button => {

//       button.onclick = () => {
//           document.querySelector("#hello").style.color = button.dataset.color;
//       }

//   });

// });
