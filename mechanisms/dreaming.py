import os
import json
import random
from mechanisms.base import BaseMechanism

class DreamingMechanism(BaseMechanism):
    name = "dreaming"
    priority = 35

    def execute(self, context):
        if not context.get("is_idle", False):
            return  # Mạng đang có hoạt động mới thì không kích hoạt giấc mơ

        print("🌙 [GIẤC MƠ SỐ - REM SLEEP] Mạng lưới tĩnh, kích hoạt chu kỳ tự suy ngẫm nội tại...")
        mem_dir = "synapses/harvested_memory"
        if not os.path.exists(mem_dir): return

        mem_files = [f for f in os.listdir(mem_dir) if f.endswith(".json")]
        if not mem_files: return

        # Chọn ngẫu nhiên một ký ức trong quá khứ để chiêm nghiệm lại
        chosen_file = random.choice(mem_files)
        try:
            with open(os.path.join(mem_dir, chosen_file), "r") as f:
                memory_data = json.load(f)
            past_decision = float(memory_data.get("decision", 0.5))
            
            # Tinh chỉnh nhẹ quyết định dựa trên ký ức quá khứ
            recalled_decision = round((context["final_decision"] * 0.8) + (past_decision * 0.2), 4)
            print(f"💭 [CHIÊM NGHIỆM KÝ ỨC] Ôn lại bài học từ {chosen_file.replace('_', '/')}: {past_decision} ──► Điều biến: {recalled_decision}")
            context["final_decision"] = recalled_decision
            context["dream_state"] = f"Dreamed_from_{chosen_file}"
        except Exception: pass
