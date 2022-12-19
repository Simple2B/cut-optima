// custom javascript
const close_flash = document.querySelector(".close");
const flash_block = document.querySelector(".hit_flash");
if (flash_block) {
  close_flash.addEventListener("click", function () {
    flash_block.classList.add("invisible");
  });
}

const validateInput = (input) => {
  const value = parseFloat(input.value).toFixed(2);
  console.log("value", value);
  if (value < 0) {
    input.value = value * -1;
  } else if (value === "NaN") {
    input.value = 0;
  } else {
    input.value = value;
  }
};

const validateInputInt = (input) => {
  const value = parseInt(input.value);
  if (value < 0) {
    input.value = value * -1;
  } else if (value === "NaN") {
    input.value = 0;
  } else {
    input.value = value;
  }
};
