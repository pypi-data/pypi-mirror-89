from jumpscale.loader import j
from jumpscale.servers.gedis.baseactor import BaseActor, actor_method
import os
import requests
import nacl.encoding
from nacl.public import Box

MARKETPLACE_URL = os.environ.get("MARKETPLACE_URL", "https://demo.testnet.grid.tf/")
CREATE_USER_ENDPOINT = "marketplace/actors/backup/init"
PUBLIC_KEY_ENDPOINT = "marketplace/actors/backup/public_key"
REPO_NAMES = ["config_backup_1", "config_backup_2"]


class Backup(BaseActor):
    @actor_method
    def repos_exist(self) -> bool:
        restic_repos = j.tools.restic.list_all()
        for repo in REPO_NAMES:
            if repo not in restic_repos:
                return False
        return True

    @actor_method
    def init(self, password, new=True) -> str:
        headers = {"Content-Type": "application/json"}
        tname = j.core.identity.me.tname
        username = j.core.identity.me.tname.split(".")[0]
        url = os.path.join(MARKETPLACE_URL, PUBLIC_KEY_ENDPOINT)
        response = requests.post(url)
        if response.status_code != 200:
            raise Exception("Can not get market place publickey")
        mrkt_pub_key = nacl.public.PublicKey(response.json().encode(), nacl.encoding.Base64Encoder)
        priv_key = j.core.identity.me.nacl.private_key
        box = Box(priv_key, mrkt_pub_key)
        password_encrypted = box.encrypt(password.encode(), encoder=nacl.encoding.Base64Encoder).decode()
        data = {"threebot_name": tname, "passwd": password_encrypted, "new": new}
        url = os.path.join(MARKETPLACE_URL, CREATE_USER_ENDPOINT)
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise j.exceptions.Value(f"can not create user with name:{username}, error={response.text}")
        config_dict = dict(zip(REPO_NAMES, response.json()))
        for repo_name, serverip in config_dict.items():
            print(repo_name, serverip)
            repo = j.tools.restic.get(repo_name)
            repo.repo = f"rest:http://{username}:{password}@{serverip}:8000/{username}/"
            repo.password = password
            repo.init_repo()
            repo.save()
        return j.data.serializers.json.dumps({"data": "backup repos inited"})

    @actor_method
    def backup(self, tags=None) -> str:
        if not self.repos_exist():
            raise j.exceptions.Value("Please configure backup first")
        if tags:
            tags = tags.split(",")
        else:
            tags = []
        tags.append(str(j.data.time.now().timestamp))
        for repo_name in REPO_NAMES:
            repo = j.tools.restic.get(repo_name)
            repo.backup(j.core.dirs.JSCFGDIR, tags=tags)
        return j.data.serializers.json.dumps({"data": "backup done"})

    @actor_method
    def snapshots(self, tags=None) -> str:
        if tags:
            tags = tags.split(",")

        snapshots = []

        for repo_name in REPO_NAMES:
            repo = j.tools.restic.get(repo_name)
            repo_snapshots = repo.list_snapshots(tags=tags)
            if repo_snapshots:
                snapshots.append(repo_snapshots)
            else:
                snapshots.append([])

        processed = set()
        result = []

        n = len(snapshots[0])
        m = len(snapshots[1])
        if snapshots:
            min_size = min(n, m)
            size = min_size if min_size < 10 else 10
            for i in range(size):
                snap_1 = snapshots[0][n - i - 1]
                snap_2 = snapshots[1][m - i - 1]

                tag_1 = snap_1.get("tags", [""])[-1]
                tag_2 = snap_2.get("tags", [""])[-1]
                if tag_1 not in processed:
                    processed.add(tag_1)
                    result.append(snap_1)

                if tag_2 not in processed:
                    processed.add(tag_2)
                    result.append(snap_2)

        return j.data.serializers.json.dumps({"data": result})

    def get_last_snapshot(self, tags=None):
        def _add_snapshot_timestamp(snapshot):
            snapshot["time"] = j.data.time.get(snapshot["time"]).timestamp
            return snapshot

        snapshots = []
        for repo_name in REPO_NAMES:
            repo = j.tools.restic.get(repo_name)
            repo_snapshots = repo.list_snapshots(last=True, tags=tags, path=j.core.dirs.JSCFGDIR)
            if repo_snapshots:
                snapshot = repo_snapshots[0]
                snapshot["repo_name"] = repo_name
                snapshots.append(snapshot)
        snapshots = list(map(_add_snapshot_timestamp, snapshots))
        if not snapshots:
            raise j.exceptions.NotFound("can not find any snapshots in the repo")
        return max(snapshots, key=lambda x: x["time"])

    @actor_method
    def restore(self, tags=None) -> str:
        if not self.repos_exist():
            raise j.exceptions.Value("Please configure backup first")
        snapshot = self.get_last_snapshot(tags=tags)
        repo = j.tools.restic.get(snapshot["repo_name"])
        repo.restore("/", snapshot_id=snapshot["id"])
        return j.data.serializers.json.dumps({"data": "repos restored"})

    @actor_method
    def enable_auto_backup(self) -> str:
        if not self.repos_exist():
            raise j.exceptions.Value("Please configure backup first")
        for repo_name in REPO_NAMES:
            repo = j.tools.restic.get(repo_name)
            repo.auto_backup(j.core.dirs.JSCFGDIR)
        return j.data.serializers.json.dumps({"data": "auto backup enabled"})

    @actor_method
    def check_auto_backup(self) -> bool:
        if not self.repos_exist():
            raise j.exceptions.Value("Please configure backup first")

        for repo_name in REPO_NAMES:
            repo = j.tools.restic.get(repo_name)
            if not repo.auto_backup_running(j.core.dirs.JSCFGDIR):
                return False
        return True

    @actor_method
    def disable_auto_backup(self) -> str:
        if not self.repos_exist():
            raise j.exceptions.Value("Please configure backup first")
        for repo_name in REPO_NAMES:
            repo = j.tools.restic.get(repo_name)
            repo.disable_auto_backup(j.core.dirs.JSCFGDIR)
        return j.data.serializers.json.dumps({"data": "auto backup disabled"})


Actor = Backup
