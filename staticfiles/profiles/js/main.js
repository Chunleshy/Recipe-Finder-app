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

    searchInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            searchRecipes();
        }
    }); 
    
});