import os
import json
from mechanisms.base import BaseMechanism

TRUST_FILE = "synapses/trust_matrix.json"

class ImmuneMechanism(BaseMechanism):
    name = "immune"
    priority = 25  # Chạy ngay sau khi thu thập xong tín hiệu

    def execute(self, context):
        harvested = context.get("harvested", {})
        trust_matrix = {}

        if os.path.exists(TRUST_FILE):
            try:
                with open(TRUST_FILE, "r") as f: trust_matrix = json.load(f)
            except Exception: pass

        # Khởi tạo điểm cho peer mới (mặc định 0.7)
        for peer in context.get("peers", []):
            if peer not in trust_matrix:
                trust_matrix[peer] = 0.7

        if not harvested:
            context["trust_matrix"] = trust_matrix
            context["quorum_decision"] = 0.5
            return

        # Tính trung vị (median) để làm mốc kháng tấn công Byzantine
        values = sorted(harvested.values())
        median_val = values[len(values)//2]

        weighted_votes = []
        total_weight = 0.0

        for peer, dec in harvested.items():
            current_trust = trust_matrix.get(peer, 0.7)
            deviation = abs(dec - median_val)

            # Phát hiện độc tố: lệch quá 0.35 so với trung vị của bầy đàn
            if deviation > 0.35:
                current_trust = max(0.05, round(current_trust * 0.75, 4))
                print(f"🚨 [HỆ MIỄN DỊCH CẢNH BÁO] Node {peer} gửi giá trị dị thường ({dec})! Giảm tín nhiệm xuống {current_trust}")
            else:
                current_trust = min(1.0, round(current_trust + 0.05, 4))

            trust_matrix[peer] = current_trust

            # Nếu điểm tín nhiệm quá thấp (< 0.2), đưa vào diện cách ly (Quarantine), không cho bỏ phiếu
            if current_trust >= 0.2:
                weighted_votes.append(dec * current_trust)
                total_weight += current_trust
            else:
                print(f"🚫 [CÁCH LY BYZANTINE] Node {peer} bị tước quyền biểu quyết vì điểm tín nhiệm quá thấp ({current_trust})!")

        # Tính phán quyết Quorum có trọng số tín nhiệm
        if total_weight > 0:
            weighted_decision = round(sum(weighted_votes) / total_weight, 4)
        else:
            weighted_decision = 0.5

        context["trust_matrix"] = trust_matrix
        context["quorum_decision"] = weighted_decision
        print(f"⚖️ [ĐỒNG THUẬN CÓ BẢO VỆ] Phán quyết Quorum có trọng số tín nhiệm: {weighted_decision}")

        # Lưu lại sổ tín nhiệm
        os.makedirs("synapses", exist_ok=True)
        with open(TRUST_FILE, "w") as f:
            json.dump(trust_matrix, f, indent=4)
