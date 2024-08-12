// http://200.123.248.223:3000
const updateAdvice = (updateSource, params = []) => {
    let URL = `http://127.0.0.1:3200/pedagogical?`;
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
    let URL = `http://127.0.0.1:3200/vocational?`;
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
    const URL = `http://127.0.0.1:3200/chat?prompt=${encodeURIComponent(query)}`;

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
    const URL = `http://127.0.0.1:8000/advices/${dni}`;

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
