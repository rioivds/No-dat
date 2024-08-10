// http://200.123.248.223:3000
const updateAdvice = (query, updateSource) => {
    const URL = 'http://127.0.0.1:3000';

    fetch(URL)
        .then (res => {
            return res.json();
        })
        .then (data => {
            updateSource(data);
        })
        .catch (e => console.error);
}

// const getData = (query, updateSource) => {
//     const API_KEY = '6iypQbKw0banGwrf4rVDWNE21L1cIShf';
//     const URL = `https://api.giphy.com/v1/gifs/search?q=${encodeURIComponent(query)}&api_key=${API_KEY}&limit=1`;

//     fetch(URL)
//         .then(res => {
//             if (!res.ok) {
//                 throw new Error('Something went bad with the API!: ' + res.statusText);
//             }
//             return res.json();
//         })
//         .then(data => {
//             updateSource(data);
//         })
//         .catch(e => {
//             console.log(e);
//         })
<<<<<<< HEAD
// }
=======
// }
>>>>>>> 164692896c26948734757e73e5c8f6950f6747c4
