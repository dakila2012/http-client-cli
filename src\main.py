import argparse
import json
import sys
import requests
def main():
    parser = argparse.ArgumentParser(description="CLI HTTP client")
    parser.add_argument("url", help="URL to request")
    parser.add_argument("--method", "-X", default="GET", help="HTTP method")
    parser.add_argument("--header", "-H", action="append", help="Custom header")
    parser.add_argument("--data", "-d", help="Request data")
    parser.add_argument("--json", "-j", help="JSON data")
    args = parser.parse_args()
    if args.json and args.data:
        parser.error("Cannot use both --json and --data")
    headers_dict = {}
    if args.header:
        for h in args.header:
            if ":" in h:
                key, value = h.split(":", 1)
                headers_dict[key.strip()] = value.strip()
    kwargs = {"timeout": 30}
    if headers_dict:
        kwargs["headers"] = headers_dict
    if args.json:
        try:
            kwargs["json"] = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(2)
    elif args.data:
        kwargs["data"] = args.data
    method = args.method.upper()
    needs_body = method not in {"GET", "HEAD", "OPTIONS", "TRACE"}
    if needs_body and "data" not in kwargs and "json" not in kwargs:
        kwargs["data"] = sys.stdin.read()
    try:
        response = requests.request(method=method, url=args.url, **kwargs)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"HTTP/1.1 {response.status_code} {response.reason}")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print()
    print(response.text)
if __name__ == "__main__":
    main()
