document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const submitBtn = document.getElementById('submitBtn');
  console.log(submitBtn);

  form.addEventListener('submit', function () {
    submitBtn.disabled = true;
    if (submitBtn.textContent == 'Submit'){
       submitBtn.textContent = 'Submitting...'
    }

    else if (submitBtn.textContent == 'Login') {
       submitBtn.textContent = 'Redirecting...'
    }

    else if (submitBtn.textContent == 'Update') {
      submitBtn.textContent = 'Updating...'
    }

    else if (submitBtn.textContent == '✉️ Send Message') {
      submitBtn.textContent = 'Sending...'
    }

    else if (submitBtn.textContent == 'Send Verification Code') {
          submitBtn.textContent = 'Sending...'
        }

    else if (submitBtn.textContent == 'Verify') {
    submitBtn.textContent = 'Verifying...'
  }

    else if (submitBtn.textContent == 'Sign up') {
    submitBtn.textContent = 'Signing...'
  }
    else if (submitBtn.textContent == 'Send SMS') {
        submitBtn.textContent = 'Sending...'
      }
    submitBtn.classList.add('animate', 'animate-pulse', 'duration-1000', 'cursor-not-allowed');
  });
});



