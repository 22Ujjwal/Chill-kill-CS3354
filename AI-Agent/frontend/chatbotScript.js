function openForm() {
    //document.getElementById("myForm").style.display = "block";
    const popup = document.getElementById("myForm");

    // Make it visible
    popup.style.display = "block";

    // Remove any previous animation classes
    popup.classList.remove("animate__bounceOutDown", "animate__animated");

    // Add the animation for opening
    popup.classList.add("animate__animated", "animate__bounceInUp");
}

function closeForm() {
    //document.getElementById("myForm").style.display = "none";
    const popup = document.getElementById("myForm");

    // Add exit animation
    popup.classList.remove("animate__bounceInUp", "animate__animated");
    popup.classList.add("animate__animated", "animate__bounceOutDown");

    // Wait for animation to finish, then hide the popup
    setTimeout(() => {
        popup.style.display = "none";
    }, 800); // duration matches the CSS animation length
}