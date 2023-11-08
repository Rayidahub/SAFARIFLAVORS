document.getElementById('food-image').addEventListener('click', function() {
  var foodId = '{{ food.id }}';
  fetchFoodDetails(foodId);
});

function fetchFoodDetails(foodId) {
  fetch('/get_food/' + foodId)
  .then(response => response.json())
  .then(data => {
      var detailsElement = document.getElementById('food-details');
      detailsElement.innerHTML = `
          <h2>${data.name}</h2>
          <p>Category: ${data.category}</p>
          <p>Country: ${data.country}</p>
          <p>Description: ${data.description}</p>
          <img src="${data.image}" alt="${data.name}">
      `;
  })
  .catch(error => console.error('Error:', error));
}