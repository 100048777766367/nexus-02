import json

class UniversalAdapter:
    """Tự động chuẩn hóa mọi gói tin từ các đời seed, monad, genome và nexus"""
    @staticmethod
    def parse_packet(raw_text):
        try:
            data = json.loads(raw_text)
        except Exception:
            return None

        decision = None
        if "decision" in data:
            decision = float(data["decision"])
        elif "synthesis_prediction" in data:
            decision = float(data["synthesis_prediction"])
        elif "command_pulse" in data and isinstance(data["command_pulse"], list):
            decision = float(data["command_pulse"][0])
        elif "features" in data and isinstance(data["features"], list):
            decision = float(data["features"][0])
        else:
            decision = 0.5

        gossip = data.get("gossip_network", [])
        features = data.get("features", [decision, round(1.0 - decision, 4)])
        if len(features) < 2:
            features = [decision, round(1.0 - decision, 4)]

        return {
            "decision": round(decision, 4),
            "features": features[:4],
            "gossip": gossip,
            "contract": data.get("contract", "legacy.packet")
        }
