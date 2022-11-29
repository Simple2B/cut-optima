// custom javascript
document.addEventListener("DOMContentLoaded", (event) => {
  const rectAddBtn = document.querySelector(".rect-add-btn");
  const rectRemoveBtn = document.querySelector(".rect-remove-last-btn");
  const addRectForm = document.querySelector(".add-rect-form");
  const addedRectsDiv = document.querySelector(".added-rects");

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
  });
});
