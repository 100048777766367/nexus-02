import subprocess
import urllib.request
import json
from mechanisms.base import BaseMechanism
from cells.linguistic_cell import LinguisticCell

class GrazeMechanism(BaseMechanism):
    name = "graze"
    priority = 10

    def execute(self, context):
        owner = context.get("owner", "100048777766367")
        wisdom_text = None

        targets = [
            f"https://github.com/{owner}/Wpesetd-AI/raw/HEAD/legacy/01_the_great_wisdom_map.md",
            f"https://github.com/{owner}/Wpesetd-AI/raw/HEAD/ontology/philosophy_ontology_v2.0.json"
        ]
        for url in targets:
            res = subprocess.run(["curl", "-s", "-L", "-f", url], capture_output=True)
            if res.returncode == 0 and len(res.stdout) > 20:
                print(f"🌾 [GRAZE] Đã gặm cỏ cội nguồn HEAD: {url.split('/')[-1]}")
                wisdom_text = res.stdout.decode('utf-8', errors='ignore')[:150]
                break

        if not wisdom_text:
            try:
                req = urllib.request.Request("https://en.wikipedia.org/api/rest_v1/page/random/summary", 
                                             headers={"User-Agent": "Nexus02-Immune-Node"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    d = json.loads(resp.read().decode())
                    wisdom_text = f"{d.get('title')}: {d.get('extract')[:120]}"
                    print(f"🌐 [GRAZE] Cào Wikipedia: {d.get('title')}")
            except Exception: pass

        if not wisdom_text:
            wisdom_text = "Nexus-02: Thực thể tự trị có hệ miễn dịch và giấc mơ số"

        context["wisdom_text"] = wisdom_text
        context["wisdom_vector"] = LinguisticCell.embed_text(wisdom_text)
