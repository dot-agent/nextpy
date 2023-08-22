(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})();

setTheme(getStoredTheme());

// Add event listener for theme switches
document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
    element.addEventListener('click', function(event) {
        const theme = event.target.getAttribute('data-bs-theme-value');
        setTheme(theme);
    });
});

// Function to get stored theme
function getStoredTheme() {
    const storedTheme = localStorage.getItem('theme');
    return storedTheme || 'auto';
}

// Function to set theme
function setTheme(theme) {
    const body = document.body;
    body.classList.remove('theme-light', 'theme-dark');

    if (theme === 'auto') {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-bs-theme', 'dark')
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme)
        }
    } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
    }

    localStorage.setItem('theme', theme);
}