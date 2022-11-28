// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const binAddBtn = document.querySelector("#bin-add-btn");
  const binSizeSelect = document.querySelector("#bin-size-select");
  const meticSystemSelect = document.querySelector(".metic-system");

  const addedBinsTable = document.querySelector(".added-bins");

  const removeBin = (e) => {
    let elementToDelete = e.target.parentNode.parentNode;
    if (e.target.tagName == "IMG") {
      elementToDelete = elementToDelete.parentNode;
    }
    elementToDelete.remove();
  };

  const addBin = (widht, height) => {
    var newBinTr = document.createElement("tr");
    newBinTr.innerHTML = `
      <th>
        <div class="input-sufix-block w-100 ${
          meticSystemSelect.value == "10" ? "cm" : "in"
        }">
          <input
            type="number"
            class="form-control added-bin-width h-42px"
            placeholder="Width"
            value=${widht}
            onfocusout="validateInput(this)"
          />
        </div>
      </th>
      <th>
        <div class="input-sufix-block w-100 ${
          meticSystemSelect.value == "10" ? "cm" : "in"
        }">
        <input
        type="number"
        class="form-control added-bin-height h-42px"
        placeholder="Height"
        value=${height}
        onfocusout="validateInput(this)"
        />
        </div>
        </th>

        <th>
        <div class="input-sufix-block w-100 pcs">
          <input
            type="number"
            class="form-control added-bin-quantity h-42px"
            placeholder="Quantity"
            value="1"
            min="1"
            onfocusout="validateInputInt(this)"
          />
        </div>
      </th>
      <th>
        <div
          class="del-bin-btn btn d-flex flex-column justify-content-center px-2 ml-2 bg-light rounded h-42px"
        >
          <img src="/static/img/trash-can.svg" alt="trash-can" />
        </div>
      </th>
    `;
    addedBinsTable.appendChild(newBinTr);

    const delButtons = document.querySelectorAll(".del-bin-btn");
    delButtons[delButtons.length - 1].addEventListener("click", removeBin);
  };

  binAddBtn.addEventListener("click", () => {
    const sizes = binSizeSelect.value.split("x");
    const divideValue = parseFloat(meticSystemSelect.value);
    meticSystemSelect.disabled = true;
    const width = parseFloat(sizes[0] / divideValue).toFixed(1);
    const height = parseFloat(sizes[1] / divideValue).toFixed(1);
    addBin(width, height);
  });
});
