const getData = (query, updateSource) => {
    const API_KEY = 'INSERT API KEY HERE';
    const URL = `https://api.giphy.com/v1/gifs/search?q=${encodeURIComponent(query)}&api_key=${API_KEY}&limit=1`;

    fetch(URL)
        .then(res => {
            if (!res.ok) {
                throw new Error('Something went bad with the API!: ' + res.statusText);
            }
            return res.json();
        })
        .then(data => {
            updateSource(data);
        })
        .catch(e => {
            console.log(e);
        })
}
