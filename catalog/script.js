
const products = [
    { name: "Laptop", price: 45000, category: "Electronics" },
    { name: "Mobile Phone", price: 18000, category: "Electronics" },
    { name: "Headphones", price: 1500, category: "Electronics" },
    { name: "T-Shirt", price: 500, category: "Clothing" },
    { name: "Jeans", price: 1200, category: "Clothing" },
    { name: "JavaScript Book", price: 400, category: "Books" },
    { name: "Python Book", price: 350, category: "Books" }
];

const productContainer = document.getElementById("products");
const searchInput = document.getElementById("search");
const categorySelect = document.getElementById("category");

// Display products
function displayProducts(items) {
    productContainer.innerHTML = "";

    if (items.length === 0) {
        productContainer.innerHTML = "<p>No products found.</p>";
        return;
    }

    items.forEach(function(product) {
        const div = document.createElement("div");
        div.className = "product";

        div.innerHTML = `
            <h3>${product.name}</h3>
            <p class="price">Price: ₹${product.price}</p>
            <p>Category: ${product.category}</p>
        `;

        productContainer.appendChild(div);
    });
}

// Search and filter products
function filterProducts() {
    const searchText = searchInput.value.toLowerCase();
    const selectedCategory = categorySelect.value;

    const filteredProducts = products.filter(function(product) {
        const matchesName = product.name.toLowerCase().includes(searchText);

        const matchesCategory =
            selectedCategory === "All" ||
            product.category === selectedCategory;

        return matchesName && matchesCategory;
    });

    displayProducts(filteredProducts);
}

// Update results when the user types or selects a category
searchInput.addEventListener("input", filterProducts);
categorySelect.addEventListener("change", filterProducts);

// Display all products when the page loads
displayProducts(products);