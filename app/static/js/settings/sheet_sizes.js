// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const sheetWidthInput = document.querySelector(".sheet-size-width");
  const sheetHeightInput = document.querySelector(".sheet-size-height");
  const sheetPriceInput = document.querySelector(".sheet-price");
  const sheetMoqInput = document.querySelector(".sheet-moq");
  const useInRowInput = document.querySelector(".use-in-row-input");
  const addSheetBtn = document.querySelector(".add-sheet-size");
  const addedSheetSizesDiv = document.querySelector(".added-sheet-sizes");

  let sheetWidth = sheetWidthInput.value;
  let sheetHeight = sheetHeightInput.value;
  let sheetPrice = sheetPriceInput.value;
  let sheetMoq = sheetMoqInput.value;
  let useInRow = useInRowInput.checked;

  const getDataFromInputs = () => {
    sheetWidth = sheetWidthInput.value;
    sheetHeight = sheetHeightInput.value;
    sheetPrice = sheetPriceInput.value;
    sheetMoq = sheetMoqInput.value;
    useInRow = useInRowInput.checked;

    if (sheetPrice === "" || sheetPrice === "NaN" || sheetPrice <= 0) {
      sheetPrice = 0;
      console.log(" sheetPrice = 0;");
    }

    if (sheetMoq === "" || sheetMoq === "NaN" || sheetMoq <= 0) {
      sheetMoq = 1;
      console.log(" sheetMoq = 1;");
    }
  };

  const validateDataFromInputs = () => {
    let isValid = true;
    if (!sheetWidth || sheetWidth == "NaN" || sheetWidth < 0) {
      iziToast.error({
        message: "Invalid new sheet width",
      });
    }
    if (!sheetHeight || sheetHeight == "NaN" || sheetHeight < 0) {
      iziToast.error({
        message: "Invalid new sheet height",
      });
    }

    return isValid;
  };

  const deleteSheetSize = async (e) => {
    const elementToDelete = e.target.parentNode;
    console.log(elementToDelete.id);
    const res = await fetch(`/settings/sheet/delete`, {
      credentials: "include",
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: elementToDelete.id,
      }),
    });
    if (res.status == 200) {
      elementToDelete.remove();
      iziToast.success({
        title: "Success",
        message: "Deleted",
      });
    } else {
      resJson = await res.json();
      console.error(resJson.message);

      iziToast.error({
        title: "Error",
        message: resJson.message,
      });
    }
  };

  const delButtons = document.querySelectorAll(".delete-sheet-size");
  delButtons.forEach((el) => {
    el.addEventListener("click", deleteSheetSize);
  });

  const addSheetToFront = (id) => {
    getDataFromInputs();

    const newSheetDiv = document.createElement("div");
    newSheetDiv.setAttribute("class", "d-flex justify-content-between mb-2");
    newSheetDiv.setAttribute("id", id);
    newSheetDiv.innerHTML = `
        <div class="input-group add-sheet-input-group w-50">
          <span class="input-group-text" id="basic-addon3">Continuous sheet/row</span>
          <div class="form-check form-switch d-flex align-items-center pl-50px border border-1 border-start-0 m-0 bg-color-disabled">
            <input
              class="form-check-input border-90 use-in-row-input"
              type="checkbox"
              ${useInRow && "checked"}
              disabled
            >
          </div>
        </div>

        <div class="input-group add-sheet-input-group w-50">
          <span class="input-group-text" id="basic-addon3">Price</span>
          <input
            class="form-control added-sheet-price mr-10px"
            placeholder="Price"
            type="number"
            disabled
            value=${parseFloat(sheetPrice)}
          >
        </div>

        <div class="input-group add-sheet-input-group w-33">
          <span class="input-group-text" id="basic-addon3">MOQ</span>
          <input
            class="form-control added-sheet-moq mr-10px"
            placeholder="MOQ"
            type="number"
            disabled
            value=${parseInt(sheetMoq)}
          >
        </div>

        <div class="d-flex">
          <input
            class="form-control added-sheet-size-width w-50"
            placeholder="Width"
            type="number"
            disabled
            value=${parseFloat(sheetWidth)}
          >
          <span class="input-group-text">x</span>
          <input
              class="form-control added-sheet-size-height w-50"
              placeholder="Height"
              type="number"
              disabled
              value=${parseFloat(sheetHeight)}
          >
        </div>


        <div class="btn rounded btn btn-danger delete-sheet-size ml-10px">Delete</div>
    `;
    addedSheetSizesDiv.appendChild(newSheetDiv);

    const delButtons = document.querySelectorAll(".delete-sheet-size");
    delButtons[delButtons.length - 1].addEventListener(
      "click",
      deleteSheetSize
    );

    sheetWidthInput.value = undefined;
    sheetHeightInput.value = undefined;
    sheetPrice.value = undefined;
    sheetMoq.value = undefined;
  };

  addSheetBtn.addEventListener("click", async () => {
    getDataFromInputs();

    isValidData = validateDataFromInputs();
    if (!isValidData) {
      return;
    }

    const res = await fetch(`/settings/sheet/create`, {
      credentials: "include",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        width: sheetWidth,
        height: sheetHeight,
        price: sheetPrice,
        moq: sheetMoq,
        use_in_row: useInRow,
      }),
    });
    if (res.status == 200) {
      resJson = await res.json();
      const id = resJson.id;
      addSheetToFront(id);
      iziToast.success({
        title: "Success",
        message: "Added",
      });
    } else {
      resJson = await res.json();
      console.error(resJson.message);

      iziToast.error({
        title: "Error",
        message: resJson.message,
      });
    }
  });

  //   // input data
  //   const addedBinsDiv = document.querySelector(".added-bins");
  //   const addedRectsDiv = document.querySelector(".added-rects");
  //   const bladeSizeInput = document.querySelector(".blade-size");
  //   const printPriceInput = document.querySelector(".print-price");
  //   const meticSystemSelect = document.querySelector(".metic-system");

  //   // output data
  //   const usedSheetsResInput = document.querySelector(".res-used-sheets");
  //   const usedAreaResInput = document.querySelector(".res-used-area");
  //   const wastedAreaResInput = document.querySelector(".res-wasted-area");
  //   const placedItemResInput = document.querySelector(".res-placed-item");
  //   const printPriceResInput = document.querySelector(".res-print-price");

  //   cleanAllBtn.addEventListener("click", () => {
  //     addedBinsDiv.innerHTML = "";
  //     addedRectsDiv.innerHTML = "";
  //     bladeSizeInput.value = 0;
  //     printPriceInput.value = 0;
  //     meticSystemSelect.disabled = false;
  //   });

  //   calculateBtn.addEventListener("click", () => {
  //     const addedBins = [];
  //     const addedRects = [];
  //     const bladeSize = parseFloat(bladeSizeInput.value);
  //     const printPrice = parseFloat(printPriceInput.value);
  //     const meticSystem = meticSystemMapping[parseFloat(meticSystemSelect.value)];

  //     for (const addedBinDiv of addedBinsDiv.children) {
  //       const widthInput = addedBinDiv.querySelector(".added-bin-width");
  //       const heightInput = addedBinDiv.querySelector(".added-bin-height");
  //       const picsInput = addedBinDiv.querySelector(".added-bin-quantity");
  //       const width = parseFloat(widthInput.value);
  //       const height = parseFloat(heightInput.value);
  //       const pics = parseInt(picsInput.value);
  //       addedBins.push({
  //         size: [width, height],
  //         pics: pics,
  //       });
  //     }

  //     for (const addedRectDiv of addedRectsDiv.children) {
  //       const widthInput = addedRectDiv.querySelector(".added-rect-width");
  //       const heightInput = addedRectDiv.querySelector(".added-rect-height");
  //       const picsInput = addedRectDiv.querySelector(".added-rect-quantity");
  //       const width = parseFloat(widthInput.value);
  //       const height = parseFloat(heightInput.value);
  //       const pics = parseInt(picsInput.value);
  //       addedRects.push({
  //         size: [width, height],
  //         pics: pics,
  //       });
  //     }

  //     console.log("bins", addedBins);
  //     console.log("rects", addedRects);
  //     console.log("bladeSize", bladeSize);
  //     console.log("printPrice", printPrice);
  //     console.log("meticSystem", meticSystem);
  //   });
});
