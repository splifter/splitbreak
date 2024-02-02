const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000; // Verwende PORT aus der Umgebung oder 3000 als Fallback

app.use(bodyParser.urlencoded({ extended: true }));
// Middleware, um die statischen Dateien zu servieren (z.B. HTML, CSS, JavaScript)
app.use(express.static('public'));

// Startseite Route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Starte den Server
app.listen(port, () => console.log(`Frontend-App läuft auf http://localhost:${port}`));