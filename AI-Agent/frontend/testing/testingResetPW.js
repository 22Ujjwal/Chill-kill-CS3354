const mockUserDatabase = {
    'id1': {
        password: 'H3Ll0$aM'
    }
};

const testReset = (oldPW, newPW, retypedNewPW) => {
    // First, validate old password
    const thisUser = Object.values(mockUserDatabase).find(
        user => user.password === oldPW 
    );
    if (!thisUser) {
        return ('Invalid password entered.');
    }

    // Password constraints validation
    const hasNumber = /[0-9]/.test(newPW);
    const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(newPW);
    const hasCapital = /[A-Z]/.test(newPW);
    const passHasSpace = /\s/.test(newPW);

    if (newPW.length < 8 || newPW.length > 32) {
        return ("Password does not meet the criteria.");
    }

    if (!hasNumber || !hasSpecialChar || !hasCapital) {
        return ("Password does not meet the criteria.");
    }

    if (passHasSpace) {
        return ("Password does not meet the criteria.");
    }

    // Check if retyped password matches password
    if (newPW !== retypedNewPW) {
        return ("Retyped password does not match.");
    }

    // Update password
    return "Password successfully updated!";
}

module.exports = testReset;