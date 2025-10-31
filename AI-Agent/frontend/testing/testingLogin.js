// Validation functions
function validateEmail(email) {
    // Check length
    if (email.length > 254) return false;
    // Check for spaces or control characters
    if (/[\s\x00-\x1F\x7F]/.test(email)) return false;
    // Check basic email format
    const emailRegex = /^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$/;
    return emailRegex.test(email);
}

// Validate username
function validateUsername(username) {
    // Check length (3-20)
    if (username.length < 3 || username.length > 20) return false;
    // Check for spaces or control characters
    if (/[\s\x00-\x1F\x7F]/.test(username)) return false;
    // Only alphanumeric
    return /^[a-zA-Z0-9]+$/.test(username);
}

// Validate password
function validatePassword(password) {
    // Check length (8-32)
    if (password.length < 8 || password.length > 32) return false;
    // Check for spaces or control characters
    if (/[\s\x00-\x1F\x7F]/.test(password)) return false;
    // Check requirements: at least 1 uppercase, 1 lowercase, 1 number, 1 special char
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[^a-zA-Z0-9]/.test(password);
    
    return hasUppercase && hasLowercase && hasNumber && hasSpecial;
}


const testLogin = (username, password) => {
    const isEmail = username.includes('@');
    if (isEmail) {
        const validUserName = validateEmail(username);
        if (!validUserName)
            return "Login failed. Username/email is invalid.";
    }
    else {
        const validUserName = validateUsername(username);
        if (!validUserName)
            return "Login failed. Username/email is invalid.";
    }

    const validPassword = validatePassword(password);
    if (!validPassword)
        return "Login failed. Password is invalid.";

    return mockLogin(username, password);

}


const mockUserDatabase = {
    'id1': {
        email: 'exists@gmail.com',
        username: 'exists',
        password: 'H3Ll0$aM'
    }
};

function mockLogin(username, password) {
    if (username.includes('@')) {
        const thisUser = Object.values(mockUserDatabase).find(
            user => user.email === username
        )
        if (thisUser == null)
            return 'Login failed. Username/email is invalid.'

        if (thisUser.password != password)
            return 'Login failed. Username/email is invalid.'
    }
    else {
        const thisUser = Object.values(mockUserDatabase).find(
            user => user.username === username
        )
        if (thisUser == null)
            return 'Login failed. Username/email is invalid.'

        if (thisUser.password != password)
            return 'Login failed. Username/email is invalid.'
    }
    return "Login successful!"
}

module.exports = testLogin;