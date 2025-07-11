hamBurger = document.getElementById('hamBurger')
hamBurgerImg = document.querySelector('#hamBurger img')
sideBar = document.getElementById('sideBar')
hamBurger.style.display = 'none'

function checkScreenSize() {
  if (window.innerWidth < 640) {
      console.log("Screen size is smaller than sm (640px)");
      hamBurger.style.display = 'block'
      hamBurgerImg.src = '../../static/assets/logo/visible.png'
  }

  else {
    hamBurger.style.display = 'none'
  }
}

checkScreenSize();

window.addEventListener("resize", checkScreenSize);


function sideBarToggle() {

  let isHidden = getComputedStyle(sideBar).display === 'none'; 

  sideBar.style.display = isHidden ? 'block' : 'none'

  hamBurgerImg.src = isHidden ? '../../static/assets/logo/hide.png' : '../../static/assets/logo/visible.png'

}



