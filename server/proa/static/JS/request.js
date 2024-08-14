// http://200.123.248.223:3200
const updateAdvice = (updateSource, params = []) => {
    let URL = `https://api.proadsrioiv.dev.ar/pedagogical?`;
    for (let i of params) {
        URL += i;
    }
    
    fetch(URL.substring(0, URL.length - 1))
        .then (res => {
            return res.json();
        })
        .then (data => {
            updateSource(data);
        })
        .catch (e => console.error);
}

const vocationalAdvice = (updateSource, params = []) => {
    let URL = `https://api.proadsrioiv.dev.ar/vocational?`;
    for (let i of params) {
        URL += i;
    }
    
    fetch(URL.substring(0, URL.length - 1))
        .then (res => {
            return res.json();
        })
        .then (data => {
            updateSource(data);
        })
        .catch (e => console.error);
}

const getChat = (query, updateChat) => {
    const URL = `https://api.proadsrioiv.dev.ar/chat?prompt=${encodeURIComponent(query)}`;

    fetch(URL)
        .then (res => {
            return res.json();
        })
        .then (data => {
            updateChat(data);
        })
        .catch (e => console.error);
}

const getCalificacionesAlumno = async dni => {
    const URL = `https://api.proadsrioiv.dev.ar/advices/${dni}`;

    const res = await fetch(URL)
        .then(res => {
            return res.json();
        })
        .then (data => {
            return data;
        })
        .catch(e => console.error);

    return res;
};
