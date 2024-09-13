
function showEncadreurDetails(applicationId) {
    var detailsDiv = document.getElementById('encadreur-details-' + applicationId);
    if (detailsDiv.style.display === "none") {
        detailsDiv.style.display = "block";
    } else {
        detailsDiv.style.display = "none";
    }
}

