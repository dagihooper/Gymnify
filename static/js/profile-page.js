const csrfToken = '{{ csrf_token }}';

const profileDiv = document.getElementById('profileDiv')
const updatingMsg = document.getElementById('updating_msg')
updatingMsg.style.display = 'none'

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
          updatingMsg.style.display = 'block'
          updatingMsg.style.position = 'fixed'

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
              updatingMsg.classList.add('bg-green-500')
              updatingMsg.textContent = 'Updated🎯'

              setTimeout(() => {

                updatingMsg.style.display = 'none'
                
              }, 3000);

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