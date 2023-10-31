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