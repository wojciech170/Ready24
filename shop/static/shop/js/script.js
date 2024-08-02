document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("dropdownButton").addEventListener("click", function () {
        const dropdownMenu = document.getElementById("dropdownMenu");
        if (dropdownMenu.style.display === "block") {
            dropdownMenu.style.display = "none";
        } else {
            dropdownMenu.style.display = "block";
        }
    });

    document.getElementById("searchButton").addEventListener("click", function () {
        const searchBox = document.getElementById("searchBox");
        if (searchBox.style.display === "block") {
            searchBox.style.display = "none";
        } else {
            searchBox.style.display = "block";
        }
    });

    window.onclick = function (event) {
        if (!event.target.matches('#dropdownButton')) {
            const dropdowns = document.getElementsByClassName("dropdown-content");
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.style.display === "block") {
                    openDropdown.style.display = "none";
                }
            }
        }

        // if (!event.target.matches('#searchButton')) {
        //     const searchBoxes = document.getElementsByClassName("search-box");
        //     for (let j = 0; j < searchBoxes.length; j++) {
        //         const openSearchBox = searchBoxes[j];
        //         if (openSearchBox.style.display === "block") {
        //             openSearchBox.style.display = "none";
        //         }
        //     }
        // }
    }
});
