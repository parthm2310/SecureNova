from collections import defaultdict, deque
from datetime import datetime, timedelta

CALL_THRESHOLD=20
WINDOW=60

class AnomalyDetector:
    def __init__(self):
        self.calls=defaultdict(deque)
        self.last_scope={}
        self.tokens={}

    def call(self,identity,t):
        q=self.calls[identity]; q.append(t)
        while q and q[0] < t-timedelta(seconds=WINDOW): q.popleft()
        if len(q)>CALL_THRESHOLD:
            self.alert("CALL_VOLUME_SPIKE",identity,f"{len(q)} requests in {WINDOW}s",t)

    def scope(self,identity,scope,t):
        prev=self.last_scope.get(identity); self.last_scope[identity]=scope
        if prev is not None and prev!=scope:
            self.alert("SCOPE_CHANGE",identity,f"{prev} -> {scope}",t)

    def issue(self,token,expiry):
        self.tokens[token]=expiry

    def use(self,token,identity,t):
        expiry=self.tokens.get(token)
        if expiry and t>expiry:
            self.alert("TOKEN_REUSE_AFTER_EXPIRY",identity,
                       f"{token} expired {expiry.isoformat()} and was reused at {t.isoformat()}",t)

    @staticmethod
    def alert(kind,identity,detail,t):
        print(f"[ALERT] [{t.isoformat(timespec='seconds')}] type={kind} identity={identity} detail=\"{detail}\"")

if __name__=="__main__":
    d=AnomalyDetector(); t0=datetime.now()
    print("=== Scenario 1: call volume spike ===")
    for i in range(25): d.call("agent_b_orchestrator_target",t0+timedelta(seconds=i*.5))
    print("\n=== Scenario 2: scope change ===")
    d.scope("agent_b_orchestrator_target","read:ai-data",t0+timedelta(seconds=30))
    d.scope("agent_b_orchestrator_target","write:admin",t0+timedelta(seconds=32))
    print("\n=== Scenario 3: token reuse after expiry ===")
    expiry=t0+timedelta(seconds=120)
    d.issue("tok_abc123",expiry)
    d.use("tok_abc123","agent_m2m_client",t0+timedelta(seconds=150))
