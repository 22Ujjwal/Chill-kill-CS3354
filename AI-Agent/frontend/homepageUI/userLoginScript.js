//Script needs to check if user is actually logged in AND needs to know the user's name.
//The back-end for the authorization could return a boolean to let this script know if user is logged in.
//Could also return the first name of the user along with it, so that it can be plugged into the
//dashboard.

//Function for displaying username in dashboard when user logs in
window.addEventListener('DOMContentLoaded', () => {
    const navbarDisplayUser = document.getElementById('navbarDisplayUser');
    const displayName = localStorage.getItem('displayName');
    console.log("Loaded display name:", displayName);
    if (displayName) {
        navbarDisplayUser.textContent = 'Welcome ' + displayName + '!';
    } else {
        navbarDisplayUser.textContent = '';
    }
});