const testLogin = require('./testingLogin');

test('Valid email and password work', () => {
  expect(testLogin("exists@gmail.com", "H3Ll0$aM")).toBe("Login successful!");
});

test('Valid email and password work', () => {
  expect(testLogin("admin234@gmail.com", "hellosam")).toBe("Login failed. Password is invalid.");
});

test('Valid email and password work', () => {
  expect(testLogin("admin234@gmail.com", "hello sam")).toBe("Login failed. Password is invalid.");
});

test('Valid email and password work', () => {
  expect(testLogin("invalid@gmail.com", "H3Ll0$aM")).toBe("Login failed. Username/email is invalid.");
});

test('Valid email and password work', () => {
  expect(testLogin("exception @ gmail.com", "H3Ll0$aM")).toBe("Login failed. Username/email is invalid.");
});