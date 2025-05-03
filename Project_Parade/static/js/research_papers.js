document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('search-input');
    const papersList = document.getElementById('papers-list');
    const originalPapers = Array.from(papersList.querySelectorAll('li')); // Store the original papers
    const dataList = document.getElementById('suggestions-list');

    // Fetch paper suggestions based on input
    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length > 0) {
            fetch(`/get_paper_suggestions?q=${query}`)
            .then(response => response.json())
            .then(data => {
                dataList.innerHTML = ''; // Clear previous suggestions

                data.forEach(paper => {
                    const option = document.createElement('option');
                    option.value = paper.title; // Assuming paper has a title property
                    dataList.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching suggestions:', error));
        } else {
            dataList.innerHTML = ''; // Clear suggestions if input is empty
        }
    });

    // Function to filter papers based on search query
    function filterPapers(query) {
        // Clear existing results
        papersList.innerHTML = '';

        // Filter the original papers based on the search query
        const filteredPapers = originalPapers.filter(paper => {
            const title = paper.textContent.toLowerCase();
            return title.includes(query.toLowerCase());
        });

        // Append filtered papers to the list
        if (filteredPapers.length > 0) {
            filteredPapers.forEach(paper => {
                papersList.appendChild(paper);
            });
        } else {
            papersList.innerHTML = '<p>No research papers found.</p>';
        }
    }

    // Add event listener for search button
    document.getElementById('search-btn').addEventListener('click', function() {
        const query = searchInput.value;
        if (query) {
            filterPapers(query);
        } else {
            resetPapers();
        }
    });

    // Function to reset papers to the original list
    function resetPapers() {
        papersList.innerHTML = '';
        originalPapers.forEach(paper => {
            papersList.appendChild(paper);
        });
    }

    // Add input event listener to reset when search is cleared
    searchInput.addEventListener('input', function() {
        if (searchInput.value === '') {
            resetPapers();
        }
    });
});