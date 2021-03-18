/* Add your Application JavaScript */
"use strict"
document.addEventListener("DOMContentLoaded", function(){
    function bankDets(evt, bank) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
          tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(bank).style.display = "block";
        evt.currentTarget.className += " active";
      }
});


