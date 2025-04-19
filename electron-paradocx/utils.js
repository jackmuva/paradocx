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
		
		// Get unique URLs from the context array
		const uniqueUrls = [...new Set(result.context.map(item => item.url))];
		
		// Create the HTML with both response content and URLs
		resultsContainer.innerHTML = `
			<div class="response-content">
				<h3>Response:</h3>
				<div>${result.response.content}</div>
			</div>
			<div class="source-urls">
				<h3>Sources (${uniqueUrls.length}):</h3>
					${uniqueUrls.map(url => `
						<a href="${url}" target="_blank">${url}</a>>
					`).join('')}
			</div>
		`;
	} catch (error) {
		resultsContainer.textContent = `Error: ${error.message}`;
	}
}


