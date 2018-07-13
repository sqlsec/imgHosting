from imgHosting.lib.base import FreeimgUpLoad

# 为了webapp/sync.py 同步到数据库，拿出 uploadsPath
import os
uploadsPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads/")

__all__ = ["FreeimgUpLoad", "uploadsPath"]