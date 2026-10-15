class BaseMechanism:
    """Khung chuẩn giao diện cắm-rút cho mọi cơ chế"""
    name = "base_mechanism"
    priority = 100

    def execute(self, context):
        raise NotImplementedError
