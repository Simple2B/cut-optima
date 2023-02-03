date = new Date();
year = date.getFullYear();
month = date.getMonth() + 1;
if (month < 10) {
  month = "0" + month;
}
document.getElementById("current_date").innerHTML =
  "© " + month + "." + year + " Copyright:All rights reserved";
