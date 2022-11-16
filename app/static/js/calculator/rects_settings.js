// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const rectAddBtn = document.querySelector("#rect-add-btn");
  const meticSystemSelect = document.querySelector(".metic-system");

  const addedRectsDiv = document.querySelector(".added-rects");

  const removeRect = (e) => {
    let elementToDelete = e.target.parentNode.parentNode;
    if (e.target.tagName == "IMG") {
      elementToDelete = elementToDelete.parentNode;
    }
    elementToDelete.remove();
  };

  const addRect = (widht, height) => {
    var newRectDiv = document.createElement("div");
    newRectDiv.setAttribute("class", "d-flex on-hover-border mb-2px");
    newRectDiv.innerHTML = `
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
            class="del-rect-btn btn d-flex flex-column justify-content-center px-2 ml-2 bg-light rounded"
        >
            <img
                src="/static/img/trash-can.svg"
                alt="trash-can"
            />
        </div>
    </div>
    `;
    addedRectsDiv.appendChild(newRectDiv);

    const delButtons = document.querySelectorAll(".del-rect-btn");
    delButtons[delButtons.length - 1].addEventListener("click", removeRect);
  };

  rectAddBtn.addEventListener("click", () => {
    meticSystemSelect.disabled = true;

    const widthInput = document.querySelector(".rect-width");
    const heightInput = document.querySelector(".rect-height");
    const width = parseFloat(widthInput.value);
    const height = parseFloat(heightInput.value);
    console.log("data", !width || !height);
    if (!width || !height) {
      alert("You must enter both width and height");
      return;
    }

    widthInput.value = "";
    heightInput.value = "";

    console.log(width, height);
    addRect(width, height);
  });
});
