// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  // millimeters in different metric systems
  const meticSystemMapping = {
    10: "centimeter",
    25.4: "inch",
  };

  const cleanAllBtn = document.querySelector(".clean-all-btn");
  const calculateBtn = document.querySelector(".calculate-btn");
  const binsResultsDiv = document.querySelector(".bins-results");
  const imagesResultDiv = document.querySelector(".images-result");

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
    iziToast.success({
      title: "Success",
      message: "Clean",
    });

    addedBinsDiv.innerHTML = "";
    addedRectsDiv.innerHTML = "";
    bladeSizeInput.value = 0;
    printPriceInput.value = 0;
    meticSystemSelect.disabled = false;
  });

  calculateBtn.addEventListener("click", async () => {
    binsResultsDiv.innerHTML = "";
    imagesResultDiv.innerHTML = "";

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

    const res = await fetch(`/calculate`, {
      credentials: "include",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        bins: addedBins,
        rectangles: addedRects,
        bladeSize: bladeSize,
        printPrice: printPrice,
        meticSystem: meticSystem,
      }),
    });
    const resJson = await res.json();
    if (res.status !== 200) {
      iziToast.error({
        position: "bottomRight",
        title: "Error",
        message: resJson.message,
      });
      return;
    }

    usedSheetsResInput.value = resJson.bins.length;
    usedAreaResInput.value = resJson.used_area;
    wastedAreaResInput.value = resJson.wasted_area;
    placedItemResInput.value = resJson.placed_items.length;
    printPriceResInput.value = resJson.print_price;

    for (let bin of resJson.bins) {
      var binResultDiv = document.createElement("div");
      binResultDiv.setAttribute("class", "bin-result pl-15px");

      binResultDiv.innerHTML = `
      <div class="bin-result pl-15px">
        <h6 class="calculator-block-title p-1 mb-1">Sheet ${bin.sizes[0]}x${bin.sizes[1]}</h6>
        <div class="mt-1">
          <div class="d-flex mb-1">
            <span class="input-group-text">Used area</span>
            <input
              class="form-control res-used-sheets"
              placeholder="Used area"
              value="${bin.used_area}"
              type="number"
              disabled
            />
          </div>
          <div class="d-flex mb-1">
            <span class="input-group-text">Wasted area</span>
            <input
              class="form-control res-wasted-area"
              placeholder="Wasted area"
              value="${bin.wasted_area}"
              type="number"
              disabled
            />
          </div>
          <div class="d-flex mb-1">
            <span class="input-group-text">Placed items</span>
            <input
              class="form-control res-placed-item"
              placeholder="Placed items"
              value="${bin.placed_items.length}"
              type="number"
              disabled
            />
          </div>
          <div class="d-flex mb-1">
            <span class="input-group-text">Print price</span>
            <input
              class="form-control res-print-price"
              placeholder="Print price"
              value="${bin.print_price}"
              type="number"
              disabled
            />
          </div>
        </div>
      </div>
      `;
      binsResultsDiv.appendChild(binResultDiv);

      var imgResultDiv = document.createElement("div");
      imgResultDiv.setAttribute(
        "class",
        "mt-3 d-flex flex-column align-items-center"
      );
      imgResultDiv.innerHTML = `
      <h5 class="mb-0">Sheet ${bin.sizes[0]}x${bin.sizes[1]}</h5>
      <img class="w-75 border border-2 rounded test-img"
        src="data:image/png;base64,${bin.image}"
        alt="calculator-result-img"
      >
      `;
      console.log("imgResultDiv", imgResultDiv);

      imagesResultDiv.appendChild(imgResultDiv);
    }
  });
});
