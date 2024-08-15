document.getElementById('openModalBtn').onclick = function() {
    document.getElementById('chatModal').style.display = 'block';
}

document.querySelector('.close-btn').onclick = function() {
    document.getElementById('chatModal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('chatModal')) {
        document.getElementById('chatModal').style.display = 'none';
    }
}
