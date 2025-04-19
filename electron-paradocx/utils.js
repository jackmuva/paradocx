async function chat(query) {
	console.log('Starting chat function with query:', query);
	try {
		const response = await fetch(`http://localhost:8000/chat?q=${encodeURIComponent(query)}`, {
			method: "GET"
		});
		const data = await response.json();
		console.log('Response data:', data);
		return data;
	} catch (error) {
		console.error('Error in chat function:', error);
		throw error;
	}
}

async function handleSearch() {
	console.log('Starting handleSearch function');
	const searchInput = document.getElementById('search-input');
	const resultsContainer = document.getElementById('results-container');

	if (!searchInput.value.trim()) {
		resultsContainer.textContent = 'Please enter a search query';
		return;
	}

	try {
		resultsContainer.textContent = 'Searching...';
		const result = await chat(searchInput.value);
		resultsContainer.textContent = result.response.content;
	} catch (error) {
		resultsContainer.textContent = `Error: ${error.message}`;
	}
}


