const csrfToken = '{{ csrf_token }}';


setTimeout(function() {
  const messageContainer = document.getElementById('message-container');
  if (messageContainer) {
    messageContainer.style.transition = 'opacity 0.5s ease'; 
    messageContainer.style.opacity = '0';
    setTimeout(() => messageContainer.remove(), 500);
  }
}, 5000);




setTimeout(function()  {
  const circleWarning = document.getElementById('circle-warning')
  circleWarning.style.opacity = '0'
  if(circleWarning){
    circleWarning.style.transition = 'opacity 0.5s ease'
    circleWarning.style.opacity = '1'
  }
}, 11000);

const profileDiv = document.getElementById('profileDiv')


document.getElementById('profileDiv').addEventListener('click', () => {
  const fileInput = document.getElementById('profilePhotoInput');
  if (fileInput) {
      fileInput.click();
  } else {
      console.error("File input element not found!");
  }
});

// Handle file selection and change the div background
document.getElementById('profilePhotoInput').addEventListener('change', function () {
  const file = this.files[0];
  if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
          const previewImage = document.getElementById('previewImage');
          previewImage.src = `${e.target.result}`;
          console.log("Div background updated.");
      };
      reader.readAsDataURL(file);

      const formData = new FormData();
      formData.append('profile_photo', file);

      fetch('/profilepage/', { 
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken, 
          },
          body: formData
      })
      .then(response => {
          if (response.ok) {
              console.log('Profile photo uploaded successfully!');
              location.reload()
          } else {
              console.error('An error occurred while uploading the photo.');
          }
      })
      .catch(error => console.error('Error:', error));
  }
});


document.getElementById('refreshPage').addEventListener('click', function() {
  location.reload();
})



