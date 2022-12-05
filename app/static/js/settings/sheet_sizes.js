// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const sheetWidthInput = document.querySelector(".sheet-size-width");
  const sheetHeightInput = document.querySelector(".sheet-size-height");
  const sheetPriceInput = document.querySelector(".sheet-price");
  const sheetMoqInput = document.querySelector(".sheet-moq");
  const addSheetBtn = document.querySelector(".add-sheet-size");
  const addedSheetSizesDiv = document.querySelector(".added-sheet-sizes");

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
    const sheetWidth = sheetWidthInput.value;
    const sheetHeight = sheetHeightInput.value;
    const sheetPrice = sheetPriceInput.value;
    const sheetMoq = sheetMoqInput.value;

    const newSheetDiv = document.createElement("div");
    newSheetDiv.setAttribute("class", "d-flex justify-content-between mb-2");
    newSheetDiv.setAttribute("id", id);
    newSheetDiv.innerHTML = `
        <div class="input-group add-sheet-input-group">
          <span class="input-group-text" id="basic-addon3">Price</span>
          <input
            class="form-control added-sheet-price mr-20px"
            placeholder="Price"
            type="number"
            disabled
            value=${parseFloat(sheetPrice)}
          >
        </div>

        <div class="input-group add-sheet-input-group">
          <span class="input-group-text" id="basic-addon3">MOQ</span>
          <input
            class="form-control added-sheet-moq mr-20px"
            placeholder="MOQ"
            type="number"
            disabled
            value=${parseInt(sheetMoq)}
          >
        </div>

        <div class="d-flex">
          <input
            class="form-control added-sheet-size-width"
            placeholder="Width"
            type="number"
            disabled
            value=${parseFloat(sheetWidth)}
          >
          <span class="input-group-text">x</span>
          <input
              class="form-control added-sheet-size-height"
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
    const sheetWidth = sheetWidthInput.value;
    const sheetHeight = sheetHeightInput.value;
    const sheetPrice = sheetPriceInput.value;
    const sheetMoq = sheetMoqInput.value;

    if (!sheetWidth || !sheetHeight || !sheetPrice || sheetPrice < 0) {
      iziToast.error({
        message: "Invalid new sheet data",
      });
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
