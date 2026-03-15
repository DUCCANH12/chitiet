from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import httpx
import json

COOKIE = (
    "SPC_F=MytQWuzGHwoUpXNW4xAsGMcxwXwxM60u; "
    "REC_T_ID=38503ae2-869c-11f0-b6ad-f6ca8346553c; "
    "SPC_CLIENTID=TXl0UVd1ekdId29Vmgiemxkvbftczwih; "
    "SPC_U=237911730; "
    "SPC_ST=.ZTVBcXRKTmhOU2lRN0lvbLHNtxIBoe1g+iPOcAA0AWJDrU+MKqAjK9hsHi/zzNGEH3TbBlBYTL9HvFbOhkuOvhRKm4zKOAqS/cAlY/Y2s5mMqUccuv/dRX3/K1fnj2T2KPG7m7FsatQ4Ju9T0H86dq9fCritmU0mtqKmWLKO7axpRzv3hrGhe7iZQM9dNGGiQfzVlKmEE5pCio/LTxpt4C9Vq1BGsjbE8fGmcoa8H6tg63UsBpX7Pj2kuzcdAKJtgA2gV5JKAS7+l4BLzaIMp0aVrs80+MRBfjP5mvnjQUk=; "
    "SPC_EC=NmRSNVpFVDRoU3lWMkcxMV4KMwByfP9QDXNxZlCLmnBn9lQ2Xga+agA8AyukFHKGI7tRCBkTw9IDB8xPHfQbzxyM0CRRtVLyiONFaDA+dydX0PsE/y7PNTsimOWwk0RpPedDAalg4+BkRSh0dSRNCatwEfEceWMsovO8IB9T/CyA1380w1DN3/NUqKlAQL3fF6JWCJZZwSWDAjDbRMTcZFhyVbk5Hs5fM63op72nMxEUPk5JuoStDI6D4/ffV1hn.ALixdsmuQnzim0hDeUu4hraUmGTlwnERl3wcbJQAuppK; "
    "SPC_R_T_IV=ZnYwWUY4TVNjUzdwRGxVVw==; "
    "SPC_T_IV=ZnYwWUY4TVNjUzdwRGxVVw==; "
    "SPC_T_ID=jxwgmajpZNCCfH5TeobwwhKLw2vIv9eRlUhfAitVmbQNomDfh4E0rcjZU4asvMUlZXMvJ5JLaowYPkpvrp6gMcaRUTXeR53I1LXTHN1qATB9VMyn2aSvj2EgSqT2uB+YPhadwpoGXZcZOBKM7gDZfYfsHDLLv4UbpgUeXdXv64U=; "
    "SPC_R_T_ID=jxwgmajpZNCCfH5TeobwwhKLw2vIv9eRlUhfAitVmbQNomDfh4E0rcjZU4asvMUlZXMvJ5JLaowYPkpvrp6gMcaRUTXeR53I1LXTHN1qATB9VMyn2aSvj2EgSqT2uB+YPhadwpoGXZcZOBKM7gDZfYfsHDLLv4UbpgUeXdXv64U=; "
    "csrftoken=zL1RjiCs8EbHYFwfOqTMfRWe0vc6xOeH; "
    "language=vi; "
    "_med=affiliates; "
    "ds=4478c2c5e2d1665f3785e6949c2a051a"
)

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "vi,en-US;q=0.9,en;q=0.8,ko;q=0.7",
    "af-ac-enc-dat": "0414d8e85d5cfd8e",
    "af-ac-enc-sz-token": "WDP95O9KDOBNPRoz8Nfdag==|7Kmu5MAKCfr2E7XqSVgpKphptpJtTuLRUJ4aXccwy1JVxeXdrm8BVZtCkhLvcajRjbChzbt0/lQJBg==|RGCT/ckxO0S/14wY|08|3",
    "affiliate-program-type": "1",
    "referer": "https://affiliate.shopee.vn/offer/product_offer",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/145.0.0.0 Safari/537.36",
    "x-sap-ri": "d8c5b669aed90a314fcd73310501dacb96bedf0005c343907206",
    "x-sz-sdk-version": "1.12.21",
    "cookie": COOKIE,
}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query params
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        def p(key, default):
            return params.get(key, [default])[0]

        page_offset = p("page_offset", "0")
        page_limit  = p("page_limit", "20")
        sort_type   = p("sort_type", "1")
        list_type   = p("list_type", "0")
        keyword     = p("keyword", "")

        url = (
            f"https://affiliate.shopee.vn/api/v3/offer/product/list"
            f"?list_type={list_type}&sort_type={sort_type}"
            f"&page_offset={page_offset}&page_limit={page_limit}&client_type=1"
        )
        if keyword:
            url += f"&keyword={keyword}"

        try:
            with httpx.Client(timeout=15) as client:
                resp = client.get(url, headers=HEADERS)
                body = resp.content
                status = resp.status_code
        except Exception as e:
            body = json.dumps({"error": str(e)}).encode()
            status = 500

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
