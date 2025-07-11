document.querySelectorAll('.otp-input').forEach((input, index, inputs) => {
  input.addEventListener('input', function (e) {
    if (this.value.length === 1 && index < inputs.length - 1) {
      inputs[index + 1].focus();
    }

    if (index === inputs.length - 1 && Array.from(inputs).every(input => input.value.length === 1)) {
      submitOTP();
    }
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Backspace' && this.value === '' && index > 0) {
      inputs[index - 1].focus();
    }
  });
});


function submitOTP() {
  const otp = Array.from(document.querySelectorAll('.otp-input')).map(input => input.value).join('');
  
  const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

  const otpForm = document.createElement('form');
  otpForm.action = 'validation';  // Adjust the endpoint where OTP is validated
  otpForm.method = 'POST';

  const otpInput = document.createElement('input');
  otpInput.type = 'hidden';
  otpInput.name = 'otp';
  otpInput.value = otp;

  const csrfInput = document.createElement('input');
  csrfInput.type = 'hidden';
  csrfInput.name = 'csrfmiddlewaretoken';
  csrfInput.value = csrfToken;

  otpForm.appendChild(otpInput);
  otpForm.appendChild(csrfInput);
  
  document.body.appendChild(otpForm);
  otpForm.submit();  // Submit the form
}


function resendOtp(){
      const changableMsg = document.getElementById('changable-msg')
      changableMsg.innerHTML = `<p class="text-gray-600 font-poppins">
      The code will be sent in ${otpTimer}sec
    </p>`
      resend_otp_timer()
}

let otpTimer = 5

function resend_otp_timer() {

  const timeinterval = setInterval(() => {
  
  if (otpTimer > 0){
    otpTimer -= 1
    console.log(otpTimer)
    const changableMsg = document.getElementById('changable-msg');
    if (changableMsg){
      changableMsg.innerHTML = `<p class="text-gray-600 font-poppins">
      The code will be sent in ${otpTimer}sec
      </p>`;
      }
    }
  
    
  else {
    clearInterval(timeinterval)
    console.log('Resend the otp now')
    const changableMsg = document.getElementById('changable-msg');
    changableMsg.innerHTML = `<p class="text-green-600 font-poppins">
            The code has been sent!
        </p>`;    
    

    fetch('resend-otp/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
  })
  
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('OTP sent successfully');
        } else {
            console.error('Failed to resend OTP:', data.message);
        }
    })
    .catch(error => {
        console.error('Error sending OTP:', error);
    });
  }

  }, 1000);

}