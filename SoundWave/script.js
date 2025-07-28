let cart = {}; // Empty cart at start

function addToCart(productName) {
  if (cart[productName]) {
    cart[productName]++;
  } else {
    cart[productName] = 1;
  }

  updateCartUI();
}

function updateCartUI() {
  const cartCount = Object.values(cart).reduce((a, b) => a + b, 0);
  document.getElementById('cart-count').textContent = cartCount;

  const cartSection = document.querySelector('#cart p');

  if (cartCount === 0) {
    cartSection.innerHTML = 'No items yet.';
  } else {
    let itemsHTML = '<ul style="list-style: disc; text-align: left; display: inline-block;">';
    for (const [product, quantity] of Object.entries(cart)) {
      itemsHTML += `<li>${product} - ${quantity} pcs</li>`;
    }
    itemsHTML += '</ul>';
    cartSection.innerHTML = itemsHTML;
  }
}

document.getElementById("contactForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form from reloading page
    alert("Thank You! We have received your message, we will contact you as soon as possible. :)");
  document.getElementById("contactForm").reset();
});