$(document).ready(function(){

    $("#location-select").change(function(){
          // Retrieve the option value and reset the count to zero
          var locationSelect = $(this).val(), count = 0;
  
          $("table tr").each(function(index) {
          if (index !== 0) {
  
              $row = $(this);
  
              var id = $row.find("td:eq(10)").text();
  
              if (id.indexOf(locationSelect) !== 0) {
                  $row.hide();
              }
              else {
                  $row.show();
                  count++;
  
              }
          }
  
      });
          var numberItems = count;
          $("#filter-select-count").text("*Results = "+count);
  
      });
        
  });
  
  
  function myFunction() {
      var input, filter, table, tr, td, i, txtValue,locationSelect;
      input = document.getElementById("myInput");
      locationSelect= $( "#location-select" ).val();
  
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
        if (tds[i2].innerHTML.toUpperCase().indexOf(filter) > -1 ) {
  
  
          // show the row
          if(tds[10].innerHTML.indexOf(locationSelect)>-1)
          tr[i].style.display = "";
  
          // skip to the next row
          continue;
  
        }
      }
    }
  }
