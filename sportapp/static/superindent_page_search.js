function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    console.log(input)
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
      var tds = tr[i].getElementsByTagName("td");

    // hide the row
    tr[i].style.display = "none";

    // loop through row cells
    for (var i2 = 1; i2 <=5; i2++) {

      // if there's a match
      if (tds[i2].innerHTML.toUpperCase().indexOf(filter) > -1) {

        // show the row
        tr[i].style.display = "";

        // skip to the next row
        continue;

      }
    }
  }
}
