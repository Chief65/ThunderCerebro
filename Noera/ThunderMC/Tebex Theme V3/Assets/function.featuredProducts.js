const setFeaturedProducts = () => {
    if (featuredProducts.size < 1 || !document.querySelector(".featured__packages") || !document.querySelector(".featured__packages--flex")) return;
    document.querySelector(".featured__packages").style.display = "block"
    const currencySymbol = "{% if basket.currency == 'USD' %}${% elseif basket.currency == 'EUR' %}€{% elseif basket.currency == 'GBP' %}£{% else %}{{ basket.currency }}{% endif %}";
    const currencyAfter = {% if basket.currency == 'EUR' %}true{% else %}false{% endif %};
    for (const [id, value] of featuredProducts) {
        const packagesContainer = document.querySelector('.featured__packages--flex')
        const { image, color, name, price, discount, discountPercent } = value
        
        const discountPercentage = Math.round(Number(discountPercent))
        const saleAmount = () => "{{ lang.featuredProductSale }}".replace("%amount%", discountPercentage)
        function isColor(str) {
            let colorRegex = /^#([0-9a-fA-F]{3}){1,2}$/;
            return colorRegex.test(str);
        }
        const formatPrice = (p) => currencyAfter ? `${p} ${currencySymbol}` : `${currencySymbol}${p}`;
        const htmlProduct = `
        <div class="featured__package triplezone__toogle--modal" id="featured__${id}" data-remote="/package/${id}">
            <div class="featured__package--circle">
                <img src="${image}" alt="${name}">
            </div>
            <div class="featured__package--text">
                <p class="featured__package__text--title">${name} 
                    {% if config("displayFeaturedProductSalePercentage") == "enabled" %} 
                        <span class="featured__sale" style="--color: ${isColor(color) ? color : "var(--main-color)"}; ${discountPercentage <= 0 && "display: none;"}">${saleAmount()}</span>
                    {% endif %}
                </p>
                <p class="featured__package__text--price">
                    ${discount > 0
                        ? `<del style="color: var(--price-original); margin-right: 5px; text-decoration: line-through;">${formatPrice(discount)}</del><span style="color: var(--price-sale);">${formatPrice(price)}</span>`
                        : `<span style="color: var(--price-normal);">${formatPrice(price)}</span>`
                    }
                </p>
            </div>
        </div>       
        `
        packagesContainer.innerHTML += htmlProduct
        const packageHtml = document.querySelector(`#featured__${id}`)
        const packageTitle = document.querySelector(`#featured__${id} .featured__package__text--title`)
        packageHtml.style.background = `${color}3F`
        packageHtml.style.borderColor = `${color}`
        packageTitle.style.color = `${color}`
    }
}
{% if page.title == "Welcome" %}
setFeaturedProducts()
{% endif %}