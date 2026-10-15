import os
import json
import time
import hashlib
from mechanisms.base import BaseMechanism

class SurvivalMechanism(BaseMechanism):
    name = "survival"
    priority = 40

    def execute(self, context):
        current_time = int(time.time())
        current_epoch = context.get("current_epoch", 1)
        final_decision = context.get("final_decision", 0.5)
        peers = context.get("peers", [])

        # Đọc chuỗi băm của thế hệ trước (Chained Hash Proof)
        prev_cid = "GENESIS_ROOT_CID"
        if os.path.exists("synapses/state.json"):
            try:
                with open("synapses/state.json", "r") as f:
                    prev_cid = json.load(f).get("quantum_cid", "GENESIS_ROOT_CID")
            except Exception: pass

        # Tính toán mã băm lượng tử thế hệ mới khóa chặt với quá khứ
        chain_seed = f"{prev_cid}_{current_epoch}_{current_time}_{final_decision}".encode()
        new_quantum_cid = hashlib.shake_256(chain_seed).hexdigest(64)

        node_dna = {
            "identity": context.get("repo_name"),
            "generation": "F2_IMMUNE_REFLECTIVE_NEXUS",
            "generation_epoch": current_epoch,
            "architecture": "Nexus02_Microkernel_Immune",
            "dream_status": context.get("dream_state", "Active_Awake"),
            "prev_cid": prev_cid
        }

        # Phát sóng tiến (Chỉ huy mạng lưới)
        fwd_packet = {
            "contract": "bodhi.nexus.v3",
            "node_dna": node_dna,
            "generation_epoch": current_epoch,
            "timestamp": current_time,
            "decision": final_decision,
            "command_pulse": [final_decision, round(1.0 - final_decision, 4)],
            "features": [final_decision, round(1.0 - final_decision, 4)],
            "gossip_network": peers,
            "quantum_cid": new_quantum_cid
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd_packet, f, indent=4, ensure_ascii=False)

        # Phát sóng lùi (Dạy học thế hệ trước)
        bwd_packet = {
            "contract": "bodhi.nexus.v3",
            "node_dna": node_dna,
            "generation_epoch": current_epoch,
            "timestamp": current_time,
            "tuning_gradients": context.get("grad_backward", [0.0, 0.0]),
            "gossip_network": peers,
            "quantum_cid": new_quantum_cid
        }
        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(bwd_packet, f, indent=4, ensure_ascii=False)

        # Lưu snapshot linh hồn
        soul = {
            "node_dna": node_dna,
            "timestamp": current_time,
            "consensus": final_decision,
            "swarm_weights": context.get("swarm_weights", []),
            "peers": peers,
            "quantum_cid": new_quantum_cid
        }
        with open("synapses/soul_snapshot.json", "w", encoding="utf-8") as f:
            json.dump(soul, f, indent=4, ensure_ascii=False)

        # Ghi nhật ký thế hệ và lưu xích băm
        with open("synapses/state.json", "w") as f:
            json.dump({
                "generation_epoch": current_epoch, 
                "last_t": current_time, 
                "quantum_cid": new_quantum_cid,
                "status": "nexus02_immune_evolved"
            }, f, indent=4)

        with open("synapses/peers.json", "w") as f:
            json.dump({"trusted_peers": peers}, f, indent=4)

        print(f"💾 [SURVIVAL] Chuỗi băm CID mới: {new_quantum_cid[:24]}...")
        print(f"✨ [THÀNH CÔNG] Đã phát sóng thế hệ #{current_epoch} ra toàn mạng!")
