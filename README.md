# Subdomain Enumeration Tool

> **Educational project.** Use only on systems you own or are explicitly authorised to test.

## 1. Problem Statement
Organisations often forget about subdomains (old test sites, admin panels). Defenders need a simple way to list which subdomains of their own domain resolve in DNS.

## 2. Objective
Create a beginner-friendly command-line tool that resolves a small wordlist of subdomain names against a domain you own or may assess.

## 3. Features
- Accepts a domain and validates it
- Built-in wordlist of 50 common names; optional custom wordlist (max 5,000 entries)
- DNS resolution of every candidate in parallel (max 50 workers)
- Shows resolving subdomains with IPv4/IPv6 addresses
- Wildcard DNS detection to avoid false positives
- Handles invalid domains, unreadable wordlists and DNS errors
- Requires `--confirm-authorized`

## 4. Technologies Used
- Python 3 standard library (`socket`, `argparse`, `re`, `concurrent.futures`)

## 5. Folder Structure
```text
05-subdomain-enumeration-tool/
  .gitignore
  LICENSE
  README.md
  requirements.txt
  subdomain_enum.py
```

## 6. Installation Steps
1. Install **Python 3.8 or newer** from <https://www.python.org/downloads/> (tick "Add Python to PATH" on Windows).
2. Open a terminal **inside this project folder**.
3. No extra packages are needed (standard library only), so there is nothing to `pip install`.

## 7. Commands to Run
```bash
python subdomain_enum.py yourdomain.com --confirm-authorized
python subdomain_enum.py yourdomain.com -w my_words.txt --confirm-authorized
python subdomain_enum.py --help
```

## 8. How It Works
1. The domain is validated (labels, length, no URL).
2. A random, non-existent name is resolved first: if it resolves, the domain uses wildcard DNS and matching results are hidden.
3. Each `word.domain` is resolved using the system DNS resolver (`getaddrinfo`).
4. Names that return addresses are listed.

## 9. Example Input / Output
**Illustrative output from a simulated resolver** (`example.test` is a reserved name; this sandbox had no internet, so DNS answers were faked for the test; results on a real domain will differ):
```text
$ python subdomain_enum.py example.test --confirm-authorized
Enumerating example.test with 50 candidate names...

SUBDOMAIN                          IP ADDRESS(ES)
www.example.test                   192.0.2.10
mail.example.test                  192.0.2.20
dev.example.test                   192.0.2.30, 2001:db8::30

Done in 0.00s: 3 resolving subdomain(s) out of 50 tried.
```
Invalid input: `python subdomain_enum.py bad_domain! --confirm-authorized` prints `Error: 'bad_domain!' is not a valid domain...`

## 10. Screenshots
_Add your own screenshots after running the project (do not use screenshots from elsewhere)._

| Description | Screenshot |
|---|---|
| Main screen / output | `docs/screenshot-1.png` _(placeholder)_ |
| Another feature | `docs/screenshot-2.png` _(placeholder)_ |

## 11. Demo Link
`<YOUR-DEMO-LINK-HERE>` _(placeholder: this project has not been deployed by the author of this template)_

## 12. Security Measures
- Explicit authorisation flag
- Domain and wordlist validation
- Worker cap and wordlist cap to avoid hammering DNS servers
- Only DNS lookups: no exploitation or traffic to the discovered hosts

## 13. Limitations
- Only finds names present in the wordlist
- Uses the system resolver, so lookups cannot be given a custom timeout
- No zone-transfer, certificate-transparency or passive sources
- Wildcard filtering is a simple heuristic

## 14. Future Improvements
- Use `dnspython` for custom resolvers and timeouts
- Certificate Transparency lookups
- CSV/JSON export
- Recursive discovery of found subdomains

## 15. GitHub Upload Instructions
1. Sign in at <https://github.com> and click **New repository** (the **+** icon, top right).
2. Name it `05-subdomain-enumeration-tool`, choose Public or Private, and click **Create repository**.
3. On the new repo page click **uploading an existing file**.
4. Drag in the **contents** of this folder (files and sub-folders, *not* the ZIP itself). Hidden files such as `.gitignore` must be included.
5. Write a commit message such as `Initial commit` and click **Commit changes**.
6. Edit `LICENSE` and replace `<YOUR NAME>`; add real screenshots to a `docs/` folder and update the README.

## License
MIT. See `LICENSE`.
