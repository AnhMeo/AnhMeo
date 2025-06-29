document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.querySelector('.menu-text');
    const navLinks = document.querySelector('.nav-links');

    menuButton.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        menuButton.textContent = navLinks.classList.contains('active') ? 'CLOSE' : 'MENU';
    });

    // Close menu when clicking a link
    navLinks.addEventListener('click', function() {
        if (window.innerWidth <= 768) {
            navLinks.classList.remove('active');
            menuButton.textContent = 'MENU';
        }
    });

    // Reset menu state when resizing window
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            navLinks.classList.remove('active');
            menuButton.textContent = 'MENU';
        }
    });
});