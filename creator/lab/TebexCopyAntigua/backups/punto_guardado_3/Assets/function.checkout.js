const modalProductId = "337671";

$(function () {
	$(".quantity-form").on("submit", function (e) {
		e.preventDefault();

		$(".quantity__item").css("opacity", "0.7");

		$(".qty-count").addClass("disabled__btn");
		$(".quantity__input").addClass("disabled__btn");

		$.ajax({
			url: "/checkout/update",
			data: $(this).serialize(),
			method: "POST",
		}).done(function (resp) {
			let q = $(resp).find("#total-cart");
			let test = $(resp).filter("#basket_items");

			function getUpdatedBasket() {
				return $.parseJSON(test.text());
			}

			for (let products in getUpdatedBasket()) {
				let each_product = getUpdatedBasket()[products];
				$(".cart__ajax--total_price").text(`${each_product.total_basket}`);
				$(".__total--basket").text(`${each_product.total_basket}`);
			}

			updateBasket(test.text());

			$(".quantity__item").css("opacity", "1");
			$(".qty-count").removeClass("disabled__btn");
			$(".quantity__input").removeClass("disabled__btn");

			$(".minus__indicator").show();
			$(".plus__indicator").show();
			$(".plus__indicator").show();
			$(".__loading--refresh").hide();
		});
	});

	$(".qty-count").on("click", function (event) {
		event.stopPropagation();

		if ($(this).attr("data-action") == "add") {
			let dataPackage = $(this).attr("data-package");

			// Construim inputul
			let dataInput = $(`.quantity__input[name="${dataPackage}"]`);

			let recentValue = parseInt($(dataInput).val());

			$(
				`.quantity__increase[data-package="${dataPackage}"] .plus__indicator`
			).hide();
			$(
				`.quantity__increase[data-package="${dataPackage}"] .__loading--refresh`
			).css("display", "inline-block");

			$(dataInput).val(recentValue + 1);

			// Dam submit la form
			$(dataInput).submit();

			return false;
		}

		if ($(this).attr("data-action") == "minus") {
			let dataPackage = $(this).attr("data-package");

			let dataInput = $(`.quantity__input[name="${dataPackage}"]`);
			let dataButton = $(`.quantity__decrease[data-package="${dataPackage}"]`);

			let recentValue = parseInt($(dataInput).val());

			if (recentValue > 1) {
				$(
					`.quantity__decrease[data-package="${dataPackage}"] .minus__indicator`
				).hide();
				$(
					`.quantity__decrease[data-package="${dataPackage}"] .__loading--refresh`
				).css("display", "inline-block");

				$(dataInput).val(recentValue - 1);

				$(dataInput).submit();
			} else {
				$(dataButton).attr("disabled", true);
			}

			return false;
		}

		if ($(this).attr("data-action") == "manual_quantity") {
			$(this).keypress(function (e) {
				e.which == 13 && $(this).submit();
			});
			return false;
		}
	});
});

const confirmationCheckBoxes = document.querySelectorAll(
	'.confirmation__checkbox input[type="checkbox"]'
);
const checkoutButton = document.querySelectorAll(".purchaseButtons");
const gatewayForm = document.querySelector(".gateway");

confirmationCheckBoxes?.forEach((checkbox) => {
	checkbox.addEventListener("click", () => {
		const areAllChecked = [...confirmationCheckBoxes].every(
			(checkbox) => checkbox.checked
		);

		checkoutButton.forEach((button) => {
			button.disabled = !areAllChecked;
		});
	});
});

const paymentGateways = document.querySelectorAll(
	".checkout__gateways--gateway input[type='radio']"
);

paymentGateways?.forEach((gateway) => {
	gateway.addEventListener("click", (e) => {
		const selectedGateway = e.target.id;
		if (selectedGateway == "crypto") {
			document.querySelector(".purchaseButtons").style.display = "none";

			document.querySelector(".cryptoButton").style.display = "block";

			return;
		}

		document.querySelector(".purchaseButtons").style.display = "block";
		document.querySelector(".cryptoButton").style.display = "none";
	});
});