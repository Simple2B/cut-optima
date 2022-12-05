document.addEventListener("DOMContentLoaded", (event) => {
  const binSizeSelect = document.querySelector(".bin-size-input");
  const priceInput = document.querySelector(".print-price");
  const costValueDiv = document.querySelector(".cost-value");
  const costMoqQtyDiv = document.querySelector(".moq-qty");

  const setCurrentPrice = () => {
    const selectedElement = binSizeSelect.options[binSizeSelect.selectedIndex];

    if (selectedElement.hasAttribute("price")) {
      const price = parseFloat(selectedElement.getAttribute("price"));
      costValueDiv.innerHTML = price;
      priceInput.value = price;

      const moq = parseInt(selectedElement.getAttribute("moq"));
      costMoqQtyDiv.innerHTML = moq;
    }
  };

  setCurrentPrice();

  binSizeSelect.addEventListener("change", () => {
    console.log("change");
    setCurrentPrice();
  });
});
