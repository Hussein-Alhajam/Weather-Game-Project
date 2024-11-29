// Extract token from query params
const params = new URLSearchParams(window.location.search);
const accessToken = params.get('access_token');

if (accessToken) {
    // Store token securely (e.g., localStorage or cookies)
    localStorage.setItem('access_token', accessToken);

    // Redirect to the main game interface
    window.location.href = '/game';
} else {
    // Handle error
    alert('Authentication failed. Please try again.');
    window.location.href = '/';
}
