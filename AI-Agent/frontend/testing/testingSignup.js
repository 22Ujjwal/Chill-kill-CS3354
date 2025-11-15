const testSignup = (username, email, password, retypedPassword) => {

    const isValidUsername = /^[a-zA-Z0-9_]{3,20}$/;

    /*
  Username constraints:
      - Lower case or upper case letters.
      - At lease one number.
      - At least 3 and less that 20 characters. 
  */
    if (!username.match(isValidUsername)) {
        return ("Account creation failed. Username is invalid");
    }

    // Basic email format check
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    if (!email.match(emailPattern)) {
        return ("Account creation failed. Email is invalid");
    }

    if (email.length > 254) {
        return ("Account creation failed. Email is invalid");
    }


    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
    const hasCapital = /[A-Z]/.test(password);
    const passHasSpace = /\s/.test(password);

    /*
    Password constraints: 
        - Less than 32 characters.
        - At least 8 characters long.
        - At least 1 number.
        - At least 1 special characters.
        - At least 1 capital letter.
        - No space.
    */
    if (password.length < 8 || password.length > 32) {
        return ("Account creation failed. Password is invalid");
    }

    if (!hasNumber) {
        return ("Account creation failed. Password is invalid");
    }

    if (!hasSpecialChar) {
        return ("Account creation failed. Password is invalid");
    }

    if (!hasCapital) {
        return ("Account creation failed. Password is invalid");
    }

    if (passHasSpace) {
        return ("Account creation failed. Password is invalid");
    }

    // Check if retyped password matches password
    if (password !== retypedPassword) {
        return ("Account creation failed. Retyped password is invalid");
    }


    return mockSignIn(email, username, password)
}

const mockUserDatabase = {
        'id1': {
            email: 'exists@gmail.com',
            username: 'invalidUser',
            password: 'H3Ll0$aM'
        }
    };

function mockSignIn(email, username, password) {
        const thisUser = Object.values(mockUserDatabase).find(
            user => user.username === username
        )
        if (thisUser != null)
            return 'Account creation failed. Username is invalid'

        const thisUser2 = Object.values(mockUserDatabase).find(
            user => user.email === email
        )
        if (thisUser2 != null)
            return 'Account creation failed. Email is invalid'

        return "Account creation successful!"

    }

    module.exports = testSignup;