// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const rectAddBtn = document.querySelector("#rect-add-btn");

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
    <div class="d-flex on-hover-border">
        <input
            type="number"
            class="left-border-0 form-control"
            placeholder="Width"
            value=${widht}
        />
        <span class="input-group-text">x</span>
        <input
            type="number"
            class="left-border-0 form-control"
            placeholder="Height"
            value=${height}
        />
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
    const widthInput = document.querySelector(".rect-width");
    const heightInput = document.querySelector(".rect-height");
    const width = parseFloat(widthInput.value);
    const height = parseFloat(heightInput.value);
    console.log("data", !width || !height);
    if (!width || !height) {
      return;
    }

    widthInput.value = "";
    heightInput.value = "";

    console.log(width, height);
    addRect(width, height);
  });
});
