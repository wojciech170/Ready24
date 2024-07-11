document.getElementById("dropdownButton").addEventListener("click", function() {
    var dropdownMenu = document.getElementById("dropdownMenu");
    if (dropdownMenu.style.display === "block") {
        dropdownMenu.style.display = "none";
    } else {
        dropdownMenu.style.display = "block";
    }
});

document.getElementById("searchButton").addEventListener("click", function() {
    var searchBox = document.getElementById("searchBox");
    if (searchBox.style.display === "block") {
        searchBox.style.display = "none";
    } else {
        searchBox.style.display = "block";
    }
});

window.onclick = function(event) {
    if (!event.target.matches('#dropdownButton')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }

    if (!event.target.matches('#searchButton')) {
        var searchBoxes = document.getElementsByClassName("search-box");
        for (var j = 0; j < searchBoxes.length; j++) {
            var openSearchBox = searchBoxes[j];
            if (openSearchBox.style.display === "block") {
                openSearchBox.style.display = "none";
            }
        }
    }
}
