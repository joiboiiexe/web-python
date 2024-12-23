from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

# HTML content for the webpage
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Push Notification Example</title>
</head>
<body>
    <h1>Push Notification Example</h1>
    <button id="notifyBtn">Send Notification</button>

    <script>
        if ('serviceWorker' in navigator && 'Notification' in window) {
            navigator.serviceWorker.register('service-worker.js').then(reg => {
                console.log('Service Worker registered:', reg);
            }).catch(err => console.error('Service Worker registration failed:', err));
        }

        function requestNotificationPermission() {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    console.log('Notification permission granted.');
                } else {
                    alert('Notification permission denied!');
                }
            });
        }

        function showNotification() {
            if (Notification.permission === 'granted') {
                navigator.serviceWorker.ready.then(reg => {
                    reg.showNotification('Hello!', {
                        body: 'This is a push notification.',
                        icon: 'https://via.placeholder.com/100',
                        tag: 'example-notification'
                    });
                });
            } else {
                alert('Please allow notifications first!');
            }
        }

        document.getElementById('notifyBtn').addEventListener('click', () => {
            requestNotificationPermission();
            showNotification();
        });
    </script>
</body>
</html>
"""

# Service Worker JavaScript content
SW_CONTENT = """self.addEventListener('install', event => {
    console.log('Service Worker installed.');
});

self.addEventListener('activate', event => {
    console.log('Service Worker activated.');
});

self.addEventListener('notificationclick', event => {
    event.notification.close();
    event.waitUntil(
        clients.openWindow('https://example.com') // Replace with your desired URL
    );
});
"""

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        elif self.path == '/service-worker.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(SW_CONTENT.encode('utf-8'))
        else:
            super().do_GET()

# Run the server
if __name__ == "__main__":
    PORT = 8000
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"Serving on http://localhost:{PORT}")
    httpd.serve_forever()
