function addCode() {
  let i = "<h3>This is the text which has been inserted by JS</h3>";

  for (let j = 0; j < 3; j++) {
    document.getElementById("add").innerHTML += i;
  }
}