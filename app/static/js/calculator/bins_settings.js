// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const binAddBtn = document.querySelector("#bin-add-btn");
  const binSizeSelect = document.querySelector("#bin-size-select");
  const meticSystemSelect = document.querySelector(".metic-system");

  const addedBinsDiv = document.querySelector(".added-bins");

  const removeBin = (e) => {
    let elementToDelete = e.target.parentNode.parentNode;
    if (e.target.tagName == "IMG") {
      elementToDelete = elementToDelete.parentNode;
    }
    elementToDelete.remove();
  };

  const addBin = (widht, height) => {
    var newBinDiv = document.createElement("div");
    newBinDiv.setAttribute("class", "d-flex on-hover-border mb-2px");
    newBinDiv.innerHTML = `
    <div class="d-flex on-hover-border w-100">
        <div class="input-sufix-block w-100 ${
          meticSystemSelect.value == "10" ? "cm" : "in"
        }">
          <input
              type="number"
              class="left-border-0 form-control"
              placeholder="Width"
              value=${widht}
          />
        </div>
        <span class="input-group-text">x</span>
        <div class="input-sufix-block w-100 ${
          meticSystemSelect.value == "10" ? "cm" : "in"
        }">
        <input
            type="number"
            class="left-border-0 form-control"
            placeholder="Height"
            value=${height}
        />
        </div>
        <div
            class="del-bin-btn btn d-flex flex-column justify-content-center px-2 ml-2 bg-light rounded"
        >
            <img
                src="/static/img/trash-can.svg"
                alt="trash-can"
            />
        </div>
    </div>
    `;
    addedBinsDiv.appendChild(newBinDiv);

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
