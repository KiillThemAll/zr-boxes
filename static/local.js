const dTC = "theme=dark; path=/;domain=.tridecagram.ru;max-age=31536000;secure;samesite=none;partitioned";
const lTC = "theme=light; path=/;domain=.tridecagram.ru;max-age=31536000;secure;samesite=none;partitioned";

addEventListener("DOMContentLoaded", () => {
  const html = document.documentElement;

  // Color theme switcher
  const switcherTextElements = document.querySelectorAll('.theme-switcher__text');
  const moonIconElements = document.querySelectorAll('.moon-icon');
  const sunIconElements = document.querySelectorAll('.sun-icon');

  const cookies = document.cookie.split(';').map((el)=>el.trim());
  let darkTheme = true;
  let foundThemeCookie = false;
  for (let i = 0; i < cookies.length; i++) {
    let pair = cookies[i].split('=');
    if (pair[0] === 'theme') {
      if (pair[1] === 'light') switchTheme();
      foundThemeCookie = true;
      break;
    }
  }
  if (!foundThemeCookie) document.cookie = dTC;

  function switchTheme () {
    darkTheme = !darkTheme;

    document.body.classList.toggle('dark-theme');

    switcherTextElements.forEach(switcherText => {
      switcherText.textContent = darkTheme ? 'Светлая тема' : 'Тёмная тема';
    });

    if (!darkTheme) {
      document.cookie = lTC;
      
      moonIconElements.forEach(moonIcon => {
        moonIcon.style.display = 'block';
      });

      sunIconElements.forEach(sunIcon => {
        sunIcon.style.display = 'none';
      });    
      html.classList.remove('html-scrollbar-dark')
      html.classList.add('html-scrollbar-light')
    } else {
      document.cookie = dTC;

      moonIconElements.forEach(moonIcon => {
        moonIcon.style.display = 'none';
      });

      sunIconElements.forEach(sunIcon => {
        sunIcon.style.display = 'block';
      });    
      html.classList.add('html-scrollbar-dark')
      html.classList.remove('html-scrollbar-light')
    }
  }

  const themeSwitchers = document.querySelectorAll('.theme-switcher, .mobile-theme-switcher');
  themeSwitchers.forEach(switcher => {switcher.addEventListener('click', switchTheme);});
});
