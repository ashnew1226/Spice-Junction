document.addEventListener("click", function (e) {

  if (e.target.classList.contains("add-to-cart-btn")) {

    const foodId = e.target.dataset.foodId;
    const csrfToken = document.getElementById("csrfToken").value;

    fetch("/ajax/add-to-cart/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: `food_id=${foodId}`
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById("cartCount").innerText = data.cart_count;
      }
    });
  }

});
