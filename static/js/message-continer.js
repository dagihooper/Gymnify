setTimeout(function() {
  const messageContainer = document.getElementById('message-container');
  if (messageContainer) {
    messageContainer.style.transition = 'opacity 0.5s ease'; 
    messageContainer.style.opacity = '0';
    setTimeout(() => messageContainer.remove(), 500);
  }
}, 5000);
