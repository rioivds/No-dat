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

// document.getElementById('sendBtn').onclick = function() {
//     const input = document.getElementById('prompt');
//     const message = input.value;
    
//     if (message.trim() !== "") {
//         const newMessage = document.createElement('div');
//         newMessage.className = 'message sent';
//         newMessage.innerHTML = '<p>' + message + '</p>';
//         document.querySelector('.messages').appendChild(newMessage);
//         input.value = '';
//         document.querySelector('.messages').scrollTop = document.querySelector('.messages').scrollHeight;
//     }
// }