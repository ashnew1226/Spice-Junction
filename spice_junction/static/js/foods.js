document.addEventListener("DOMContentLoaded", function () {

  const buttons = document.querySelectorAll(".category-btn");

  buttons.forEach(btn => {
    btn.addEventListener("click", function () {

      /* ACTIVE BUTTON HIGHLIGHT */
      buttons.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      const categoryId = this.dataset.categoryId;
      const wrapper = document.getElementById("foodCarouselWrapper");

      wrapper.innerHTML = `<p class="text-center">Loading...</p>`;

      fetch(`/ajax/foods/${categoryId}/`)
        .then(res => res.json())
        .then(data => {

          if (data.foods.length === 0) {
            wrapper.innerHTML = "<p class='text-center'>No food available.</p>";
            return;
          }

          let carouselItems = "";

          data.foods.forEach((food, index) => {

            if (index % 4 === 0) {
              carouselItems += `
                <div class="carousel-item ${index === 0 ? 'active' : ''}">
                  <div class="row g-3 justify-content-center">
              `;
            }

            carouselItems += `
              <div class="col-md-3">
                <div class="food-card card shadow-sm h-100">
                  <div class="food-img-wrapper">
                    <img src="${food.image}" class="food-img" alt="${food.name}">
                  </div>
                  <div class="card-body text-center">
                    <h6 class="food-title">${food.name}</h6>
                    <p class="food-price">₹${food.price}</p>
                    <button class="btn btn-sm btn-success add-to-cart-btn"
                            data-food-id="${food.id}">
                    Add to Cart
                    </button>
                  </div>
                </div>
              </div>
            `;

            if ((index + 1) % 4 === 0 || index === data.foods.length - 1) {
              carouselItems += `
                  </div>
                </div>
              `;
            }

          });

          /* 🔥 RENDER CAROUSEL + BUTTONS TOGETHER */
          wrapper.innerHTML = `
            <div id="foodCarousel" class="carousel slide" data-bs-ride="false">
              <div class="carousel-inner">
                ${carouselItems}
              </div>
            </div>

            <div class="text-center mt-3">
              <button class="btn btn-sm btn-outline-dark mx-2"
                      data-bs-target="#foodCarousel"
                      data-bs-slide="prev">
                <i class="fas fa-chevron-left"></i>
              </button>

              <button class="btn btn-sm btn-outline-dark mx-2"
                      data-bs-target="#foodCarousel"
                      data-bs-slide="next">
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>
          `;

        });
    });
  });

  /* ✅ AUTO LOAD FIRST CATEGORY */
  if (buttons.length > 0) {
    buttons[0].click();
  }

});
document.addEventListener("click", function (e) {

  const button = e.target.closest(".add-to-cart-btn");

  if (button) {

    e.preventDefault(); // 🔥 IMPORTANT

    const foodId = button.dataset.foodId;
    const csrfToken = document.getElementById("csrfToken").value;

    fetch("/ajax/add-to-cart/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: `food_id=${foodId}`
    })
    .then(response => {
        if (response.status === 401) {
          window.location.href = "/accounts/login/?next=" + window.location.pathname;
          return;
        }
        return response.json();
      })
    .then(data => {
      console.log(data);

      if (data.success) {
        document.getElementById("cartCount").innerText = data.cart_count;

        button.innerText = "Added ✓";
        button.classList.remove("btn-success");
        button.classList.add("btn-secondary");

        setTimeout(() => {
          button.innerText = "Add to Cart";
          button.classList.remove("btn-secondary");
          button.classList.add("btn-success");
        }, 1000);
      }

    })
    .catch(error => console.error("Cart error:", error));
  }

});
