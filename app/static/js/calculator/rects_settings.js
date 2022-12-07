// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const rectAddBtn = document.querySelector(".rect-add-btn");
  const rectRemoveBtn = document.querySelector(".rect-remove-last-btn");
  const addRectForm = document.querySelector(".add-rect-form");
  const addedRectsDiv = document.querySelector(".added-rects");
  const totalRectsSpan = document.querySelector(".total-rects");

  const calculateTotalRestsQty = () => {
    const rectQtyInputs = document.querySelectorAll(".rect-qty");
    let totalRestsQty = 0;
    rectQtyInputs.forEach((el) => {
      if (parseInt(el.value)) {
        totalRestsQty = totalRestsQty + parseInt(el.value);
      }
    });
    totalRectsSpan.innerHTML = totalRestsQty;
    console.log("totalRestsQty", totalRestsQty);
  };

  const rectQtyInputs = document.querySelectorAll(".rect-qty");
  rectQtyInputs.forEach((el) => {
    el.addEventListener("input", () => {
      calculateTotalRestsQty();
    });
  });

  rectRemoveBtn.addEventListener("click", () => {
    const elements = document.querySelectorAll(".add-rect-form");
    if (elements.length === 1) {
      iziToast.info({
        message: "You cannot remove the last item",
      });
      return;
    }
    elements[elements.length - 1].remove();
    iziToast.success({
      message: "Removed",
    });
    calculateTotalRestsQty();
  });

  rectAddBtn.addEventListener("click", () => {
    const cloneAddRectForm = addRectForm.cloneNode(true);
    const inputs = cloneAddRectForm.querySelectorAll("input");
    inputs.forEach((element) => {
      element.value = undefined;
    });
    addedRectsDiv.appendChild(cloneAddRectForm);
    iziToast.success({
      message: "Added",
    });
    const rectQtyInputs = document.querySelectorAll(".rect-qty");
    rectQtyInputs[rectQtyInputs.length - 1].addEventListener("input", () => {
      calculateTotalRestsQty();
    });
  });
});
