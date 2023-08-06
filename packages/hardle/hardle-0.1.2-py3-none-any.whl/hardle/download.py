import os
import json
import urllib.request
from urllib.error import HTTPError


def download(har_path: str, out_path: str) -> None:
    with open(har_path, "r") as hf:
        content = json.loads(hf.read())

    entries = [e for e in content["log"]["entries"] if e["request"]["method"] == "GET"]

    opener = urllib.request.build_opener()
    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0)"
            "Gecko/20100101 Firefox/84.0",
        )
    ]
    urllib.request.install_opener(opener)

    for entry in entries:
        url: str = entry["request"]["url"]

        if not url.startswith("http"):
            # TODO: Support websockets?
            continue

        ok_req = urllib.request.Request(url, method="HEAD")

        try:
            urllib.request.urlopen(ok_req)
        except HTTPError as e:
            if e.code == 405:
                pass
            else:
                continue

        mime = entry["response"]["content"].get("mimeType", "")

        safe_path = url.split("://", 1)[1]

        long_path = next((p for p in safe_path.split("/") if len(p) > 255), None)

        if long_path:
            continue

        filename = safe_path.split("/")[-1]
        # FIXME: Maybe use urlparse for this instead?
        filename = "".join(filename.replace("#", "?").split("?", 1)[0])

        if "text/html" in mime and not filename.endswith(".html"):
            path = filename + "/" if filename != "" else ""
            filename = path + "index.html"

        path = os.path.join(out_path, "/".join([*safe_path.split("/")[:-1], filename]))

        os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            urllib.request.urlretrieve(url, path)
        except IsADirectoryError:
            # index.html does not have a mime type!
            urllib.request.urlretrieve(url, path + "/index.html")
