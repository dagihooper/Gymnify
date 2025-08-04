/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
  './userMember/templates/**/*.html',
  './userAdmin/templates/**/*.html',
  './vote/templates/**/*.js',
  './validation/templates/**/*.html',
  './homePage/templates/**/*.html',
  './validation/templates/**/*.js',
  './exercises/templates/**/*.html',


],

  theme: {
    fontSize: {
      xs: ['12px', '16px'],
      sm: ['14px', '20px'],
      base: ['16px', '19.5px'],
      lg: ['18px', '21.94px'],
      xl: ['20px', '24.38px'],
      '2xl': ['24px', '29.26px'],
      
      '3xl': ['28px', '50px'],
      '4xl': ['48px', '58px'],
      '8xl': ['96px', '106px']
    },
    extend: {
      fontFamily: {
        palanquin: ['Palanquin', 'sans-serif'],
        montserrat: ['Montserrat', 'sans-serif'],
        poppins: ['Poppins', 'sans-serif'],
        lato: ['Lato', 'sans-serif']
      },
      
      colors: {
        'primary': "#ECEEFF",
        "coral-red": "#FF6452",
        "slate-gray": "#6D6D6D",
        "pale-blue": "#F5F6FF",
        "button": "#ff777c",
        "bright-green": '#28A745',
        "blue-violet":"#5932EA",
        "light-gray": "#8A8888",
        "soft-teal": "#5ED4B8",
        "stroke": "#00B087",
        "active-text" : "#008767"
      },
      boxShadow: {
        '3xl': '0 10px 40px rgba(0, 0, 0, 0.1)'
      },
      backgroundImage: {
        'hero': "url('../../static/assets/images/background-login.png')",
        'card': "url('assets/images/thumbnail-background.svg')",
      },
      screens: {
        "wide": "1440px",
        "custom":"846px",
        "side-bar":"785px",
        "card": "1044px",
        "scroll": "660px"
      },

    },
  },
  plugins: [],
};