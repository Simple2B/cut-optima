// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const rectAddBtn = document.querySelector("#rect-add-btn");
  const meticSystemSelect = document.querySelector(".metic-system");

  const addedRectsTable = document.querySelector(".added-rects");

  const removeRect = (e) => {
    let elementToDelete = e.target.parentNode.parentNode;
    if (e.target.tagName == "IMG") {
      elementToDelete = elementToDelete.parentNode;
    }
    elementToDelete.remove();
  };

  const addRect = (widht, height) => {
    var newRectTr = document.createElement("tr");
    newRectTr.innerHTML = `
      <th>
        <div class="input-sufix-block w-100 ${
          meticSystemSelect.value == "10" ? "cm" : "in"
        }">
          <input
            type="number"
            class="left-border-0 form-control added-rect-width h-42px"
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
          class="left-border-0 form-control added-rect-height h-42px"
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
            class="form-control added-bin-height h-42px"
            placeholder="Quantity"
            value="1"
            onfocusout="validateInputInt(this)"
          />
        </div>
      </th>
      <th>
        <div
          class="del-rect-btn btn d-flex flex-column justify-content-center px-2 ml-2 bg-light rounded"
        >
          <img src="/static/img/trash-can.svg" alt="trash-can" />
        </div>
      </th>
    `;

    addedRectsTable.appendChild(newRectTr);

    const delButtons = document.querySelectorAll(".del-rect-btn");
    delButtons[delButtons.length - 1].addEventListener("click", removeRect);
  };

  rectAddBtn.addEventListener("click", () => {
    meticSystemSelect.disabled = true;

    const widthInput = document.querySelector(".rect-width");
    const heightInput = document.querySelector(".rect-height");
    const width = parseFloat(widthInput.value);
    const height = parseFloat(heightInput.value);
    if (!width || !height) {
      alert("You must enter both width and height");
      return;
    }

    widthInput.value = "";
    heightInput.value = "";

    addRect(width, height);
  });
});
