document.addEventListener("DOMContentLoaded", function() {
    const searchBox = document.getElementById('searchBox');
    const suggestionsContainer = document.getElementById('suggestions');
    const searchForm = document.getElementById("searchForm");

    let suggestions = [];

    // Event listener for input in the search box
    searchBox.addEventListener('input', function() {
        const query = this.value;
        if (query.length >= 2) {
            fetchSuggestions(query);
            searchBox.classList.add('autocomplete-active');
        } else {
            suggestionsContainer.innerHTML = '';
            searchBox.classList.remove('autocomplete-active');
        }
    });

    // Fetch suggestions based on the query
    function fetchSuggestions(query) {
        fetch(`/search?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestions = data;
                displaySuggestions(data);
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
            });
    }

    // Display suggestions in the suggestions container
    function displaySuggestions(data) {
        suggestionsContainer.innerHTML = '';

        data.forEach(item => {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = item.label;
            li.setAttribute('data-id', item.value);

            // Click event for each suggestion item
            li.addEventListener('click', function() {
                const trackId = this.getAttribute('data-id');
                searchBox.value = this.textContent;  // Set the selected suggestion in the input box
                suggestionsContainer.innerHTML = '';  // Clear suggestions
                searchBox.classList.remove('autocomplete-active');
                
                // Manually trigger the form submission after setting the value
                searchForm.action = `/result/${trackId}`;
                searchForm.submit();
            });

            suggestionsContainer.appendChild(li);
        });
    }

    // Event listener for form submission
    searchForm.addEventListener("submit", function(event) {
        const input = searchBox.value;
        const selectedSuggestion = suggestions.find(suggestion => suggestion.label === input);

        if (!selectedSuggestion) {
            alert("Please select a track from the dropdown!");
            event.preventDefault();  // Prevent form submission if the input is invalid
        } else {
            console.log("Form is submitting with input:", input);
            event.preventDefault();  // Prevent the default form submission
            
            // Redirect to the selected track's result page
            window.location.href = `/result/${selectedSuggestion.value}`;
        }
    });
});