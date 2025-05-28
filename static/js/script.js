// Function to show the route in Google Maps
function showMap() {
    const email = document.getElementById("email").value;
    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;

    // Basic validation
    if (!email.includes("@")) {
        alert("Please enter a valid email.");
        return;
    }
    if (!start || !destination) {
        alert("Please enter both locations.");
        return;
    }

    // Generate the URL for Google Maps
    const mapUrl = `https://www.google.com/maps/dir/${encodeURIComponent(start)}/${encodeURIComponent(destination)}`;

    // Open the map in a new tab
    window.open(mapUrl, '_blank');
}

// Dark Mode Toggle Function
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("dark-mode", document.body.classList.contains("dark-mode"));
}

// Load dark mode preference from local storage
window.onload = () => {
    if (localStorage.getItem("dark-mode") === "true") {
        document.body.classList.add("dark-mode");
    }

    // Add event listener to the 'Show Route' button
    const showRouteBtn = document.getElementById("showRouteBtn");
    if (showRouteBtn) {
        showRouteBtn.addEventListener("click", showMap);
    }
};
