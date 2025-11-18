const testLogin = require('./testingLogin');
const testSignup = require("./testingSignup");

test('Valid email and valid password', () => {
  expect(testLogin("exists@gmail.com", "H3Ll0$aM")).toBe("Login successful!");
});

test('Valid email and invalid password', () => {
  expect(testLogin("exists@gmail.com", "hellosam")).toBe("Login failed. Password is invalid.");
});

test('Valid email and exception causing password', () => {
  expect(testLogin("exists@gmail.com", "hello sam")).toBe("Login failed. Password is invalid.");
});

test('Invalid email and valid password', () => {
  expect(testLogin("invalid@gmail.com", "H3Ll0$aM")).toBe("Login failed. Username/email is invalid.");
});

test('Exception causing email and valid password', () => {
  expect(testLogin("exception @ gmail.com", "H3Ll0$aM")).toBe("Login failed. Username/email is invalid.");
});


test('Valid username, valid email, valid password, same retyped password', () => {
  expect(testSignup("validUser", "notexists@gmail.com", "H3Ll0$aM", "H3Ll0$aM")).toBe("Account creation successful!");
});

test('Valid username, valid email, valid password, invalid retyped password', () => {
  expect(testSignup("validUser", "notexists@gmail.com", "H3Ll0$aM", "hellosam")).toBe("Account creation failed. Retyped password is invalid");
});


test('Valid username, valid email, invalid password', () => {
  expect(testSignup("validUser", "notexists@gmail.com", "hellosam", "hellosam")).toBe("Account creation failed. Password is invalid");
});

test('Valid username, valid email, invalid password', () => {
  expect(testSignup("validUser", "notexists@gmail.com", "Hello sam", "Hello sam")).toBe("Account creation failed. Password is invalid");
});


test('Valid username, valid email, invalid password', () => {
  expect(testSignup("validUser", "exists@gmail.com", "H3Ll0$aM", "H3Ll0$aM")).toBe("Account creation failed. Email is invalid");
});

test('Valid username, valid email, invalid password', () => {
  expect(testSignup("validUser", "exception @ gmail.com", "H3Ll0$aM", "H3Ll0$aM")).toBe("Account creation failed. Email is invalid");
});

test('Valid username, valid email, invalid password', () => {
  expect(testSignup("inva_lidU*ser", "notexists@gmail.com", "H3Ll0$aM", "H3Ll0$aM")).toBe("Account creation failed. Username is invalid");
});

test('Valid username, valid email, invalid password', () => {
  expect(testSignup("invalidUser", "notexists@gmail.com", "H3Ll0$aM", "H3Ll0$aM")).toBe("Account creation failed. Username is invalid");
});

test('Valid username, valid email, invalid password', () => {
  expect(testSignup("invalid user", "notexists@gmail.com", "H3Ll0$aM", "H3Ll0$aM")).toBe("Account creation failed. Username is invalid");
});

test('valid old password, valid new password, valid retyped password', () => {
  expect(testReset("H3Ll0$aM", "H311ow0rld!", "H311ow0rld!")).toBe("Password successfully updated!");
});

test('invalid old password, valid new password, valid retyped password', () => {
  expect(testReset("hi", "H311ow0rld!", "H311ow0rld!")).toBe("Invalid password entered.");
});

test('exceptional old password, valid new password, valid retyped password', () => {
  expect(testReset("Hello sam", "H311ow0rld!", "H311ow0rld!")).toBe("Invalid password entered.");
});

test('valid old password, invalid new password, invalid retyped password', () => {
  expect(testReset("H3Ll0$aM", "helloworld", "helloworld")).toBe("Password does not meet the criteria.");
});

test('valid old password,exceptional new password, exceptional retyped password', () => {
  expect(testReset("H3Ll0$aM", "hello world!", "hello world!")).toBe("Password does not meet the criteria.");
});

test('valid old password, valid new password, invalid retyped password', () => {
  expect(testReset("H3Ll0$aM", "H311ow0rld!", "Cat123$")).toBe("Retyped password does not match.");
});
