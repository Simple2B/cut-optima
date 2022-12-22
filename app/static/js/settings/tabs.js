// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const tabSheetsBtn = document.querySelector(".settings-sheet");
  const tabSqrsBtn = document.querySelector(".settings-sqr");
  const printPriceBlockDiv = document.querySelector(".print-price-block");
  const moqSqrBlockDiv = document.querySelector(".moq-sqr-block");
  const sheetSizesDiv = document.querySelector(".sheet-sizes");

  const showAll = () => {
    printPriceBlockDiv.classList.remove("d-none");
    moqSqrBlockDiv.classList.remove("d-none");
    sheetSizesDiv.classList.remove("hide-sheet-price-blocks");
  };

  const showSheetsSettings = () => {
    showAll();
    printPriceBlockDiv.classList.add("d-none");
    moqSqrBlockDiv.classList.add("d-none");
  };

  const showSqrsSettings = () => {
    showAll();

    sheetSizesDiv.classList.add("hide-sheet-price-blocks");
  };

  tabSheetsBtn.addEventListener("click", () => {
    tabSqrsBtn.classList.remove("selected-tab-btn");
    tabSheetsBtn.classList.add("selected-tab-btn");
    showSheetsSettings();
  });
  tabSqrsBtn.addEventListener("click", () => {
    tabSqrsBtn.classList.add("selected-tab-btn");
    tabSheetsBtn.classList.remove("selected-tab-btn");
    showSqrsSettings();
  });
});
