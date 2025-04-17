const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    const filePath = path.join(__dirname, 'index.html');

    fs.readFile(filePath, (err, data) => {
        if (err) {
            console.error('Error reading the file:', err); // Log the error
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end('Error loading page');
        } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(data);
        }
    });
});

server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
