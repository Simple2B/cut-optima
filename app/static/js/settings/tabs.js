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
    tabSqrsBtn.classList.remove("btn-primary");
    tabSqrsBtn.classList.add("btn-outline-primary");
    tabSheetsBtn.classList.remove("btn-outline-primary");
    tabSheetsBtn.classList.add("btn-primary");
    showSheetsSettings();
  });
  tabSqrsBtn.addEventListener("click", () => {
    tabSqrsBtn.classList.add("btn-primary");
    tabSqrsBtn.classList.remove("btn-outline-primary");
    tabSheetsBtn.classList.add("btn-outline-primary");
    tabSheetsBtn.classList.remove("btn-primary");
    showSqrsSettings();
  });
});
