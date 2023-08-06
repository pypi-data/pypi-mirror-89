from dataclasses import dataclass


@dataclass
class Migration:
    identifier: str
    version: int
    target_version: int
    query: str

    def __str__(self):
        return f"{self.identifier} [{self.version}=>{self.target_version}]"

    def execution_string(self):
        direction = "u"
        if self.target_version < self.version:
            direction = "d"
        return f"{self.version}/{direction}  {self.identifier}"
