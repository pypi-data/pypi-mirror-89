from jumpscale.core.base import Base, fields
from enum import Enum
import hashlib


class ThreebotState(Enum):
    RUNNING = "RUNNING"  # the workloads are deployed and running
    DELETED = "DELETED"  # workloads and backups deleted
    STOPPED = "STOPPED"  # expired or manually stoped (delete workloads only)


class UserThreebot(Base):
    # instance name is the f"threebot_{solution uuid}"
    solution_uuid = fields.String()
    identity_tid = fields.Integer()
    name = fields.String()
    owner_tname = fields.String()  # owner's tname in TF Connect after cleaning
    farm_name = fields.String()
    state = fields.Enum(ThreebotState)
    continent = fields.String()
    explorer_url = fields.String()
    threebot_container_wid = fields.Integer()
    trc_container_wid = fields.Integer()
    reverse_proxy_wid = fields.Integer()
    subdomain_wid = fields.Integer()
    secret_hash = fields.String()

    def verify_secret(self, secret):
        if not self.secret_hash:
            return True
        return self.secret_hash == hashlib.md5(secret.encode()).hexdigest()

    def hash_secret(self, secret):
        self.secret_hash = hashlib.md5(secret.encode()).hexdigest()
