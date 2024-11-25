


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

//Product_list page 
function addToCart(productId) {
    fetch(`/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ productId: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('Item added to cart successfully!');
        } else {
            alert('Something went wrong. Please try again.');
        }
    });
}
///////////////////////////////

function showMessage(message) {
    const messageBox = document.createElement('div');
    messageBox.className = 'alert alert-success';
    messageBox.innerText = message;
    messageBox.style.position = 'fixed';
    messageBox.style.top = '20px';
    messageBox.style.right = '20px';
    messageBox.style.zIndex = '1000';

    document.body.appendChild(messageBox);

    setTimeout(() => {
        messageBox.remove();
    }, 5000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


///////////////////////////////

document.getElementById('subscriptionForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var email = document.getElementById('emailSubscription').value;
    fetch('/subscribe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: 'emailSubscription=' + encodeURIComponent(email)
    })
    .then(response => response.text())
    .then(data => {
        alert(data);
        window.location.href = '/';  
    });
});

///////////////////////////////
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var messageContainer = document.getElementById('message-container');
        if (messageContainer) {
            messageContainer.style.display = 'none';
        }
    }, 3000);  // Set to 3 seconds
});
