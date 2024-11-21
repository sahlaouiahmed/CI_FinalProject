function addToCart() {
    // Add to cart functionality to be added later
    alert('Product added to cart (functionality to be implemented)');
}


// JavaScript to handle the active class
document.addEventListener('DOMContentLoaded', function() {
    var currentPath = window.location.pathname;
    var homeLink = document.getElementById('home-link');
    var seedsSuppliesLink = document.getElementById('seeds-supplies-link');
    var articlesLink = document.getElementById('articles-link');
    var contactLink = document.getElementById('contact-link');

    if (currentPath === '/') {
        homeLink.classList.add('active');
    } else if (currentPath.startsWith('/store/products/')) {
        seedsSuppliesLink.classList.add('active');
    } else if (currentPath === '/articles/' || currentPath.startsWith('/articles/')) {
        articlesLink.classList.add('active');
    } else if (currentPath === '/contact/' || currentPath.startsWith('/contact')) {
        contactLink.classList.add('active');
    }
});

//Script to Update Year 
document.addEventListener('DOMContentLoaded', function() {
    var currentYear = new Date().getFullYear();
    document.getElementById('currentYear').textContent = currentYear;
});
