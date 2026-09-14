document.addEventListener("DOMContentLoaded", () => {
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  const links = document.querySelectorAll('.top-nav a[href^="#"]');
  const sections = [...links]
    .map(link => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  const onScroll = () => {
    let current = "";
    for (const section of sections) {
      if (window.scrollY >= section.offsetTop - 130) current = section.id;
    }
    links.forEach(link => {
      link.classList.toggle("active", link.getAttribute("href") === `#${current}`);
    });
  };

  document.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
});
