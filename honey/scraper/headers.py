# 1. Chrome on Windows 10
HEADERS_1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}

# 2. Firefox on Windows 10
HEADERS_2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) "
                  "Gecko/20100101 Firefox/115.0",
    "Referer": "https://www.bing.com/",
    "Connection": "keep-alive",
}

# 3. Microsoft Edge on Windows 11
HEADERS_3 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
    "Referer": "https://www.duckduckgo.com/",
    "Connection": "keep-alive",
}

# 4. Safari on macOS
HEADERS_4 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-us",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Referer": "https://www.apple.com/",
    "Connection": "keep-alive",
}

# 5. Chrome on macOS
HEADERS_5 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Referer": "https://www.reddit.com/",
    "Connection": "keep-alive",
}

# 6. Firefox on Ubuntu Linux
HEADERS_6 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) "
                  "Gecko/20100101 Firefox/115.0",
    "Referer": "https://www.mozilla.org/",
    "Connection": "keep-alive",
}

# 7. Opera on Windows
HEADERS_7 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36 OPR/99.0.0.0",
    "Referer": "https://www.opera.com/",
    "Connection": "keep-alive",
}

# 8. iPhone Safari (iOS 17)
HEADERS_8 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Referer": "https://www.apple.com/",
    "Connection": "keep-alive",
}

# 9. Chrome on Android
HEADERS_9 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}

# 10. Samsung Internet on Android
HEADERS_10 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-S918U) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "SamsungBrowser/24.0 Chrome/114.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.samsung.com/",
    "Connection": "keep-alive",
}

HEADERS = [
    HEADERS_1,HEADERS_2,HEADERS_3,
    HEADERS_4,HEADERS_5,HEADERS_6,
    HEADERS_7,HEADERS_8,HEADERS_9,HEADERS_10
]