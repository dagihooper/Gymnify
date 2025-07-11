qr_code = document.getElementById('qr_code')
overlay = document.querySelector('.overlay')
qr_displayer = document.getElementById('qr_displayer')
qr_code.addEventListener('click', 

  function() {
    
    qr_displayer.style.display = 'flex'
    overlay.style.display = 'block'

  }
)

function removeOLPE() {
    qr_displayer.style.display = 'none'
    overlay.style.display = 'none'
  
}
