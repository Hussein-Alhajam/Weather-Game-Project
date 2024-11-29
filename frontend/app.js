const express = require('express');
const path = require('path');

const app = express();
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve HTML templates
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'templates/index.html')));
app.get('/login', (req, res) => res.sendFile(path.join(__dirname, 'templates/login.html')));
app.get('/register', (req, res) => res.sendFile(path.join(__dirname, 'templates/register.html')));
app.get('/room', (req, res) => res.sendFile(path.join(__dirname, 'templates/room.html')));

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Frontend server running on http://localhost:${PORT}`));
