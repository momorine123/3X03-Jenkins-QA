  
// Script to open and close sidebar
function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}
 
function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}

// Modal Image Gallery
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  let captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}

//Asset List Table
$(document).ready(function () {
  $('#assetListTable').DataTable({

  });
});

//Requested List Table
$(document).ready(function () {
  $('#requestedListTable').DataTable({});
});

//Request To Table for manager
$(document).ready(function () {
  $('#requestToTable').DataTable({});
});

//Request FROM for manager
$(document).ready(function () {
  $('#requestFromTable').DataTable({});
});

//Admin table to add, edit, delete asset
$(document).ready(function () {
  $('#manageAssetTable').DataTable({});
});

//SELECT Asset List Table
$(document).ready(function () {
  $('#selectAssetTable').DataTable({});
});

//Admin table to manage users
$(document).ready(function () {
  $('#manageUserTable').DataTable({

  });
});



$(document).ready(function () {
  $('#manageInvList').DataTable({});
});