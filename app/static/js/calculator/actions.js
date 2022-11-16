// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const cleanAllBtn = document.querySelector(".clean-all-btn");
  const addedBinsDiv = document.querySelector(".added-bins");
  const addedRectsDiv = document.querySelector(".added-rects");
  const bladeSizeInput = document.querySelector(".blade-size");
  const printPriceInput = document.querySelector(".print-price");
  const meticSystemSelect = document.querySelector(".metic-system");

  cleanAllBtn.addEventListener("click", () => {
    addedBinsDiv.innerHTML = "";
    addedRectsDiv.innerHTML = "";
    bladeSizeInput.value = 0;
    printPriceInput.value = 0;
    meticSystemSelect.disabled = false;
  });
});
