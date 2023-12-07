

document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const searchResultsContainer = document.getElementById('search-results-container');

    const searchRecipes = () => {
        const query = searchInput.value.trim();

        if (query !== '') {
            // Make a request to your Django backend's search_recipes endpoint
            fetch(`/api/search_recipes/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Update the results container with the received data
                    searchResultsContainer.innerHTML = '';

                    if (data.length > 0) {
                        data.forEach(recipe => {
                            const recipeCard = document.createElement('div');
                            recipeCard.innerHTML = `
                                <h2>${recipe.title}</h2>
                                ${recipe.image ? `<img src="${recipe.image}" alt="${recipe.title}">` : ''}
                                <a href="${recipe.url}" target="_blank" class="view-details-button">View Recipe</a>
                            `;
                            searchResultsContainer.appendChild(recipeCard);
                        });
                    } else {
                        searchResultsContainer.innerHTML = '<p>No recipes found.</p>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching search results:', error);
                    searchResultsContainer.innerHTML = '<p>Error fetching recipes. Please try again later.</p>';
                });
        } else {
            searchResultsContainer.innerHTML = '<p>Please enter a search query.</p>';
        }
    };

    searchButton.addEventListener('click', searchRecipes);

    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            searchRecipes();
        }
    });
 
    const showRecipeDetails = (recipeId) => {
        // Make a request to the Edamam API or your backend to get detailed information
        fetch(`/api/get_recipe_details/?id=${recipeId}`)
            .then(response => response.json())
            .then(recipeDetails => {
                // Display the detailed information in a modal or a new section on your page
                const modal = document.createElement('div');
                modal.classList.add('recipe-details-modal');
                modal.innerHTML = `
                    <h2>${recipeDetails.title}</h2>
                    ${recipeDetails.image ? `<img src="${recipeDetails.image}" alt="${recipeDetails.title}">` : ''}
                    <h3>Ingredients:</h3>
                    <ul>
                        ${recipeDetails.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
                    </ul>
                    <h3>Instructions:</h3>
                    <p>${recipeDetails.instructions}</p>
                    <button class="close-modal-button">Close</button>
                `;
                document.body.appendChild(modal);

                // Add event listener to close the modal
                const closeModalButton = modal.querySelector('.close-modal-button');
                closeModalButton.addEventListener('click', () => {
                    document.body.removeChild(modal);
                });
            })
            .catch(error => {
                console.error('Error fetching recipe details:', error);
                // Handle error, e.g., display an error message
         });
    };
   

    data.forEach(recipe => {
        console.log('Recipe ID:', recipe.id);
        const recipeCard = document.createElement('div');
        recipeCard.innerHTML = `
            <h2>${recipe.title}</h2>
            ${recipe.image ? `<img src="${recipe.image}" alt="${recipe.title}">` : ''}
            <p>${recipe.description}</p>
            <button class="view-details-button" data-recipe-id="${recipe.id}">View Details</button>
        `;
        searchResultsContainer.appendChild(recipeCard);

        // Add event listener to the "View Details" button
        const detailsButton = recipeCard.querySelector('.view-details-button');
        detailsButton.addEventListener('click', () => {
            showRecipeDetails(recipe.id);
        });
    });
});