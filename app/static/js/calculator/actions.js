// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  // millimeters in different metric systems
  const meticSystemMapping = {
    cm: "M",
    in: "FT",
  };

  const calculateBtn = document.querySelector(".calculate-btn");
  const imagesResultDiv = document.querySelector(".images-result");

  // input data
  const bladeSizeInput = document.querySelector(".blade-size");
  const printPriceInput = document.querySelector(".print-price");
  const meticSystemSelect = document.querySelector(".metic-system");

  // output data
  const metricResDiv = document.querySelector(".metric-res");
  const sheetSizeResDiv = document.querySelector(".sheet-size-res");
  const usageResQtyDiv = document.querySelector(".usage-res-qty");
  const usageMetricResDiv = document.querySelector(".usage-metric-res");
  const usageMetricDiv = document.querySelector(".usage-metric");
  const availableResQtyDiv = document.querySelector(".available-res-qty");
  const availableResPerUnitDiv = document.querySelector(
    ".available-res-per-unit"
  );
  const availableMetricResDiv = document.querySelector(".available-metric-res");
  const totalCostResDiv = document.querySelector(".total-cost-res");
  const costResDiv = document.querySelector(".cost-res");

  calculateBtn.addEventListener("click", async () => {
    // binsResultsDiv.innerHTML = "";
    imagesResultDiv.innerHTML = "";
    let addedBins = [];
    let binWidth = 0;
    let binHeight = 0;

    const binSizeInput = document.querySelector(".bin-size-input");
    if (binSizeInput.tagName === "DIV") {
      const binSizeWidhtInput = binSizeInput.querySelector(".bin-width");
      binWidth = parseFloat(binSizeWidhtInput.value);
      const binSizeHeightInput = binSizeInput.querySelector(".bin-height");
      binHeight = parseFloat(binSizeHeightInput.value);
    } else {
      const binSizeInputValue = binSizeInput.value;
      const splitedValue = binSizeInputValue.split("x");
      binWidth = parseFloat(splitedValue[0]);
      binHeight = parseFloat(splitedValue[1]);
    }

    if (!binWidth || !binHeight || binWidth < 1 || binHeight < 1) {
      iziToast.error({
        message: "Incorrect sheet sizes",
      });
      return;
    }

    addedBins.push({
      size: [binWidth, binHeight],
      pics: 1,
    });

    const addedRects = [];

    const addedRectDivs = document.querySelectorAll(".add-rect-form");
    for (const addedRectDiv of addedRectDivs) {
      const widthInput = addedRectDiv.querySelector(".rect-width");
      const heightInput = addedRectDiv.querySelector(".rect-height");
      const picsInput = addedRectDiv.querySelector(".rect-qty");
      const width = parseFloat(widthInput.value);
      const height = parseFloat(heightInput.value);
      const pics = parseInt(picsInput.value);
      if (!width || !height || width < 1 || height < 1) {
        iziToast.error({
          message: "Incorrect artwork sizes",
        });
        return;
      }
      addedRects.push({
        size: [width, height],
        pics: pics,
      });
    }

    const bladeSize = parseFloat(bladeSizeInput.value);
    const printPrice = parseFloat(printPriceInput.value);
    const meticSystem = meticSystemSelect.value;

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

    metricResDiv.innerHTML = meticSystem;
    usageResQtyDiv.innerHTML = resJson.used_area.toFixed(1);
    usageMetricResDiv.innerHTML = "SQR";
    usageMetricDiv.innerHTML = meticSystemMapping[meticSystem];

    availableResQtyDiv.innerHTML = resJson.wasted_area.toFixed(1);
    totalCostResDiv.innerHTML = resJson.print_price.toFixed(2) + "$";
    availableMetricResDiv.innerHTML = meticSystemMapping[meticSystem];
    availableResPerUnitDiv.innerHTML = "SQR";
    costResDiv.innerHTML = printPriceInput.value + "$";

    for (let bin of resJson.bins) {
      var imgResultDiv = document.createElement("div");

      sheetSizeResDiv.innerHTML = `${bin.sizes[0]}x${bin.sizes[1]}`;

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
