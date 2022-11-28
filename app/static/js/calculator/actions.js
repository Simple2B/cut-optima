// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  // millimeters in different metric systems
  const meticSystemMapping = {
    10: "centimeter",
    25.4: "inch",
  };

  const cleanAllBtn = document.querySelector(".clean-all-btn");
  const calculateBtn = document.querySelector(".calculate-btn");

  // input data
  const addedBinsDiv = document.querySelector(".added-bins");
  const addedRectsDiv = document.querySelector(".added-rects");
  const bladeSizeInput = document.querySelector(".blade-size");
  const printPriceInput = document.querySelector(".print-price");
  const meticSystemSelect = document.querySelector(".metic-system");

  // output data
  const usedSheetsResInput = document.querySelector(".res-used-sheets");
  const usedAreaResInput = document.querySelector(".res-used-area");
  const wastedAreaResInput = document.querySelector(".res-wasted-area");
  const placedItemResInput = document.querySelector(".res-placed-item");
  const printPriceResInput = document.querySelector(".res-print-price");

  cleanAllBtn.addEventListener("click", () => {
    addedBinsDiv.innerHTML = "";
    addedRectsDiv.innerHTML = "";
    bladeSizeInput.value = 0;
    printPriceInput.value = 0;
    meticSystemSelect.disabled = false;
  });

  calculateBtn.addEventListener("click", () => {
    const addedBins = [];
    const addedRects = [];
    const bladeSize = parseFloat(bladeSizeInput.value);
    const printPrice = parseFloat(printPriceInput.value);
    const meticSystem = meticSystemMapping[parseFloat(meticSystemSelect.value)];

    for (const addedBinDiv of addedBinsDiv.children) {
      const widthInput = addedBinDiv.querySelector(".added-bin-width");
      const heightInput = addedBinDiv.querySelector(".added-bin-height");
      const picsInput = addedBinDiv.querySelector(".added-bin-quantity");
      const width = parseFloat(widthInput.value);
      const height = parseFloat(heightInput.value);
      const pics = parseInt(picsInput.value);
      addedBins.push({
        size: [width, height],
        pics: pics,
      });
    }

    for (const addedRectDiv of addedRectsDiv.children) {
      const widthInput = addedRectDiv.querySelector(".added-rect-width");
      const heightInput = addedRectDiv.querySelector(".added-rect-height");
      const picsInput = addedRectDiv.querySelector(".added-rect-quantity");
      const width = parseFloat(widthInput.value);
      const height = parseFloat(heightInput.value);
      const pics = parseInt(picsInput.value);
      addedRects.push({
        size: [width, height],
        pics: pics,
      });
    }

    console.log("bins", addedBins);
    console.log("rects", addedRects);
    console.log("bladeSize", bladeSize);
    console.log("printPrice", printPrice);
    console.log("meticSystem", meticSystem);
  });
});
