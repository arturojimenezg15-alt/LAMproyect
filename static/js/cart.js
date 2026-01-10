document.addEventListener('DOMContentLoaded', function() {
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Attach click event to all add-to-cart buttons
    // Note: use delegation if products are loaded dynamically
    document.body.addEventListener('click', function(e) {
        if (e.target.closest('.add-to-cart')) {
            e.preventDefault();
            const btn = e.target.closest('.add-to-cart');
            const productId = btn.dataset.productId;
            const url = btn.dataset.url;
            const imgSrc = btn.dataset.image;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    
                    // Animate
                    animateFlyToCart(btn, imgSrc);

                    // Update Badge
                    const badge = document.getElementById('cart-badge');
                    if (badge) {
                        badge.innerText = data.cart_total;
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    function animateFlyToCart(btn, imgSrc) {
        if (!imgSrc) return;

        const cartIcon = document.getElementById('cart-icon-container');
        if (!cartIcon) return;

        const img = document.createElement('img');
        img.src = imgSrc;
        img.classList.add('cart-fly-img');
        
        const rect = btn.getBoundingClientRect();
        img.style.top = rect.top + 'px';
        img.style.left = rect.left + 'px';
        
        document.body.appendChild(img);

        const cartRect = cartIcon.getBoundingClientRect();

        // Force reflow
        img.offsetHeight; 

        // Move to cart
        img.style.top = cartRect.top + 'px';
        img.style.left = cartRect.left + 'px';
        img.style.width = '20px';
        img.style.height = '20px';
        img.style.opacity = '0';

        setTimeout(() => {
            img.remove();
        }, 1000);
    }
});
