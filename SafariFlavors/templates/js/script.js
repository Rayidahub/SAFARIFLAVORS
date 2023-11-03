$(document).ready(function(){
 $("#search-button").click(function(){
    var searchTerm = $("#search-input").val();
    // Use the searchTerm variable to filter the list of recipes
 });
});

$(document).ready(function(){
 $(".food-image").click(function(){
    // Retrieve the information about the selected food and display it in the modal window
 });
});

document.querySelectorAll('.category-item').forEach(category => {
   category.addEventListener('click', function() {
       let currentCategory = this.textContent;
       // Change images according to the selected category
   });
});

document.querySelectorAll('.country-item').forEach(country => {
   country.addEventListener('click', function() {
       let currentCountry = this.textContent;
       // Change images according to the selected country
   });
});

// Get the modal
var modal = document.getElementById("myModal");
    
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var foodImages = document.getElementsByClassName("food-images")[0].getElementsByTagName("img");
for (var i = 0; i < foodImages.length; i++) {
    foodImages[i].onclick = function() {
        modal.style.display = "block";
        document.getElementById("food-name").innerHTML = this.alt;
        document.getElementById("food-description").innerHTML = "Description for " + this.alt;
    }
}