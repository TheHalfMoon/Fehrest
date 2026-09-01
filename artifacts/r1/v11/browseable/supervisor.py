#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys, tarfile
from collections import Counter
from pathlib import Path

EXPECTED_HEAD="ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c"
EXPECTED_ARMING_SHA="2e360072931ac2adfbdbba94da20d9198f8b24474852429545bcd14cd8653205"
EXPECTED_V11_DIGEST="5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2"
EXPECTED_RUNNER_DIGEST="30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f"
EXPECTED_BUNDLE_SHA="17934f84a07afef08e469b0526d343d26e5597ea3455e575b5f9c46ae91c321e"
SEED="r1-x1-f10c4a673c44d412adb9c4f5a495d4c38265ce38301a778128b0fab622ed8a04"
RUNNER_VERSION="r1-external-runner/1.1.0"

USER=Path.home()
REPO=USER/"OneDrive"/"Desktop"/"Fehrest"
BASE=Path(os.environ.get("LOCALAPPDATA",str(USER/"AppData"/"Local")))/"Fehrest"/"R1-X1"
SOURCE=BASE/"variance-pilot-599054280a96"
INCIDENTS=BASE/"incidents"
CONTROL=BASE/"replacement-current.json"
LOCK_PATH=BASE/"variance-pilot-single-runner.lock"
FORENSICS=BASE/"forensics"
DESKTOP=USER/"OneDrive"/"Desktop"
if not DESKTOP.is_dir(): DESKTOP=USER/"Desktop"
RESULT=DESKTOP/"FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt"

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(Path(p).read_bytes())
def cjson(o): return (json.dumps(o,sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
def write_once(path,data):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_bytes()!=data: raise RuntimeError(f"write-once mismatch: {path}")
    else: path.write_bytes(data)

def load_jsonl(path):
    out=[]
    path=Path(path)
    if not path.is_file(): return out
    for n,line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(),1):
        if not line.strip(): continue
        x=json.loads(line)
        if not isinstance(x,dict): raise RuntimeError(f"non-object JSONL {path}:{n}")
        out.append(x)
    return out

def audit(root):
    root=Path(root)
    records=load_jsonl(root/"records.jsonl")
    order=load_jsonl(root/"execution-order.jsonl")
    rids=[str(x.get("run_id","")) for x in records]
    oids=[str(x.get("run_id","")) for x in order]
    if any(not x for x in rids+oids): raise RuntimeError("missing run_id")
    rawids=sorted(p.stem for p in (root/"raw").glob("*.txt")) if (root/"raw").is_dir() else []
    rc,oc=Counter(rids),Counter(oids)
    rs,oset,raws=set(rids),set(oids),set(rawids)
    return dict(
        record_count=len(rids),raw_count=len(rawids),order_entry_count=len(oids),
        duplicate_record_ids=sorted(k for k,v in rc.items() if v>1),
        duplicate_order_ids=sorted(k for k,v in oc.items() if v>1),
        orphan_raw=sorted(raws-rs),record_missing_raw=sorted(rs-raws),
        order_without_record=sorted(oset-rs),record_without_order=sorted(rs-oset),
        ok_records=sum(1 for r in records if r.get("outcome")=="OK"),
        task_failure_records=sum(1 for r in records if r.get("outcome")=="TASK_FAILURE"),
        infra_failure_records=sum(1 for r in records if r.get("outcome")=="INFRASTRUCTURE_FAILURE"),
        model_returned_values=sorted({str(r.get("model_returned")) for r in records if r.get("model_returned") not in (None,"UNAVAILABLE")}),
    )

def git(*args):
    p=subprocess.run(["git","-C",str(REPO),*args],text=True,capture_output=True)
    if p.returncode: raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout.strip()

def verify_repo():
    if git("rev-parse","HEAD")!=EXPECTED_HEAD: raise RuntimeError("HEAD mismatch")
    if git("status","--porcelain"): raise RuntimeError("worktree dirty")
    v=REPO/"bench"/"R1"/"verify_v1_1.py"
    p=subprocess.run([sys.executable,str(v)],cwd=REPO,text=True,capture_output=True)
    t=p.stdout+p.stderr
    if p.returncode: raise RuntimeError("verify_v1_1 failed: "+t[-3000:])
    for x in ("V1_1_SEMANTIC_FREEZE_STATUS=PASS",EXPECTED_V11_DIGEST,EXPECTED_RUNNER_DIGEST,EXPECTED_BUNDLE_SHA):
        if x not in t: raise RuntimeError(f"v1.1 binding missing: {x}")

def raw_manifest_digest(rawdir):
    files=sorted(Path(rawdir).glob("*.txt"),key=lambda p:p.name)
    payload="".join(f"{sha_file(p)}  raw/{p.name}\n" for p in files).encode()
    return sha_bytes(payload),len(files)

def latest_forensic():
    if not FORENSICS.is_dir(): return None
    xs=sorted((p for p in FORENSICS.glob("variance-pilot-599054280a96-*") if p.is_dir()),key=lambda p:p.name)
    return xs[-1] if xs else None

def prepare():
    try:
        os.environ.pop("OPENAI_API_KEY",None)
        verify_repo()
        arming=SOURCE/"ARMING-MANIFEST.json"
        preflight=SOURCE/"preflight.json"
        runroot=SOURCE/"runs"/"variance-pilot"
        if sha_file(arming)!=EXPECTED_ARMING_SHA: raise RuntimeError("source arming digest mismatch")
        arm=json.loads(arming.read_text(encoding="utf-8-sig"))
        checks={
            "canonical_commit":EXPECTED_HEAD,
            "r1_v1_1_digest":EXPECTED_V11_DIGEST,
            "runner_fileset_sha256":EXPECTED_RUNNER_DIGEST,
            "external_bundle_sha256":EXPECTED_BUNDLE_SHA,
            "randomization_seed":SEED,
            "total_sessions":888,
        }
        for k,v in checks.items():
            if arm.get(k)!=v: raise RuntimeError(f"source arming mismatch {k}")
        if sha_file(preflight)!=arm.get("preflight_record_sha256"): raise RuntimeError("preflight digest mismatch")
        a=audit(runroot)
        exp=dict(record_count=109,raw_count=109,order_entry_count=112,duplicate_record_ids=[],
                 duplicate_order_ids=["vm-000021","vm-000022"],orphan_raw=[],record_missing_raw=[],
                 order_without_record=["vm-000059"],record_without_order=[])
        for k,v in exp.items():
            if a[k]!=v: raise RuntimeError(f"source state moved: {k} observed={a[k]!r} expected={v!r}")
        rawsha,rawcount=raw_manifest_digest(runroot/"raw")
        f=latest_forensic(); froot=None; fmsha=None
        if f:
            fm=f/"SHA256SUMS.txt"
            if fm.is_file(): froot=str(f); fmsha=sha_file(fm)
        incident={
            "schema":"fehrest-r1-x1-execution-incident/1",
            "stage":"R1-VARIANCE-PILOT",
            "source_batch":str(SOURCE),
            "source_canonical_commit":EXPECTED_HEAD,
            "source_arming_manifest_sha256":EXPECTED_ARMING_SHA,
            "source_records_sha256":sha_file(runroot/"records.jsonl"),
            "source_execution_order_sha256":sha_file(runroot/"execution-order.jsonl"),
            "source_execution_plan_sha256":sha_file(runroot/"execution-plan.json"),
            "source_state_binding_sha256":sha_file(runroot/"state-binding.json"),
            "source_raw_manifest_sha256":rawsha,
            "source_raw_count":rawcount,
            "source_record_count":a["record_count"],
            "source_order_entry_count":a["order_entry_count"],
            "duplicate_order_ids":a["duplicate_order_ids"],
            "order_without_record":a["order_without_record"],
            "forensic_snapshot_root":froot,
            "forensic_hash_manifest_sha256":fmsha,
            "failure_class":"INFRASTRUCTURE_CONCURRENCY_EVIDENCE_BREACH",
            "reason":"Two concurrent sealed runners wrote the same PilotRoot. Realized order contains duplicate transport-attempt identifiers and one ordered attempt without an immutable raw/record pair. The sealed protocol makes realized order permanent evidence and requires every attempt to be recorded; deleting or deduplicating these lines would conceal execution history.",
            "disposition":"INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE",
            "raw_outputs_preserved_unchanged":True,
            "scoring_performed":False,"unblinding_performed":False,"confirmatory_performed":False,
            "replacement_design_change":False,"replacement_seed_change":False,
            "replacement_model_condition_change":False,"replacement_uses_same_v1_1_protocol":True,
            "decision_basis_is_execution_integrity_not_observed_arm_score":True,
            "replacement_model_calls_at_declaration":0,
        }
        ib=cjson(incident); isha=sha_bytes(ib)
        ip=INCIDENTS/f"R1-X1-INCIDENT-{isha[:12]}.json"; write_once(ip,ib)
        repl=BASE/f"variance-pilot-replacement-{isha[:12]}"; repl.mkdir(parents=True,exist_ok=True)
        extract=repl/"external-bundle"; broot=extract/"r1-external"
        archive=REPO/"bench"/"R1"/"dist"/"r1-external-bundle.tar.gz"
        if sha_file(archive)!=EXPECTED_BUNDLE_SHA: raise RuntimeError("bundle archive digest mismatch")
        if not broot.is_dir():
            if extract.exists() and any(extract.iterdir()): raise RuntimeError("partial replacement bundle exists")
            extract.mkdir(parents=True,exist_ok=True)
            with tarfile.open(archive,"r:gz") as tf: tf.extractall(extract)
        if not (broot/"BUNDLE-MANIFEST.txt").is_file(): raise RuntimeError("replacement bundle invalid")
        rp=repl/"preflight.json"
        if rp.exists():
            if rp.read_bytes()!=preflight.read_bytes(): raise RuntimeError("replacement preflight differs")
        else: shutil.copyfile(preflight,rp)
        rm={
            "schema":"fehrest-r1-x1-replacement-arming/1",
            "status":"ARMED_REPLACEMENT_FOR_INVALIDATED_INFRASTRUCTURE_BATCH",
            "incident_sha256":isha,"incident_path":str(ip),"invalidated_source_batch":str(SOURCE),
            "canonical_commit":EXPECTED_HEAD,"r1_v1_1_digest":EXPECTED_V11_DIGEST,
            "runner_fileset_sha256":EXPECTED_RUNNER_DIGEST,"external_bundle_sha256":EXPECTED_BUNDLE_SHA,
            "preflight_record_sha256":sha_file(rp),"runner_version":RUNNER_VERSION,
            "model_requested":arm.get("model_requested"),"model_returned":arm.get("model_returned"),
            "model_version_pin_status":arm.get("model_version_pin_status"),
            "reasoning_effort":arm.get("reasoning_effort"),"max_output":int(arm.get("max_output")),
            "temperature_status":arm.get("temperature_status"),"top_p_status":arm.get("top_p_status"),
            "model_seed_status":arm.get("model_seed_status"),
            "randomization_seed_method":arm.get("randomization_seed_method"),"randomization_seed":SEED,
            "order_algorithm":arm.get("order_algorithm"),
            "maintenance_sessions":168,"continuation_sessions":720,"total_sessions":888,
            "model_calls_at_replacement_seal":0,"scoring_status":"NOT_STARTED",
            "unblinding_status":"NOT_STARTED","confirmatory_status":"NOT_STARTED",
        }
        rmb=cjson(rm); rmp=repl/"REPLACEMENT-ARMING-MANIFEST.json"; write_once(rmp,rmb)
        control={"incident_sha256":isha,"incident_path":str(ip),"replacement_root":str(repl),
                 "replacement_arming_manifest_sha256":sha_file(rmp),"seed":SEED}
        CONTROL.write_bytes(cjson(control))
        print("PREPARE_STATUS=PASS")
        print(f"INCIDENT_SHA256={isha}")
        print("SOURCE_BATCH_STATUS=INVALIDATED_INFRASTRUCTURE_CONCURRENCY")
        print(f"REPLACEMENT_ROOT={repl}")
        print(f"REPLACEMENT_ARMING_MANIFEST_SHA256={sha_file(rmp)}")
        print("REPLACEMENT_MODEL_CALLS_EXECUTED=0")
        return 0
    except Exception as e:
        RESULT.write_text("=== FEHREST R1-X1 REPLACEMENT PREPARE FAILURE ===\n"
                          f"FAILURE_REASON={type(e).__name__}: {e}\nMODEL_CALLS_EXECUTED=0\n"
                          "SCORING_STATUS=NOT_STARTED\nUNBLINDING_STATUS=NOT_STARTED\n"
                          "CONFIRMATORY_STATUS=NOT_STARTED\n",encoding="utf-8")
        print(f"PREPARE_STATUS=FAIL\nFAILURE_REASON={type(e).__name__}: {e}")
        return 1

def acquire_lock():
    import msvcrt
    LOCK_PATH.parent.mkdir(parents=True,exist_ok=True)
    f=open(LOCK_PATH,"a+b",buffering=0); f.seek(0,2)
    if f.tell()==0: f.write(b"\0")
    f.seek(0)
    try: msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
    except OSError:
        f.close(); raise RuntimeError("another R1 pilot supervisor holds the global lock")
    return f

def run_cmd(cmd,cwd,out,err,env=None):
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    with open(out,"w",encoding="utf-8",newline="\n") as fo, open(err,"w",encoding="utf-8",newline="\n") as fe:
        p=subprocess.Popen(cmd,cwd=cwd,stdout=fo,stderr=fe,text=True,env=env)
        return p.wait()

def kv(text):
    d={}
    for line in text.splitlines():
        if "=" in line:
            k,v=line.split("=",1)
            if k and " " not in k: d[k.strip()]=v.strip()
    return d

def write_result(lines): RESULT.write_text("\n".join(lines)+"\n",encoding="utf-8")

def run():
    lock=None
    try:
        if not os.environ.get("OPENAI_API_KEY","").startswith("sk-"): raise RuntimeError("API key absent")
        c=json.loads(CONTROL.read_text(encoding="utf-8")); repl=Path(c["replacement_root"]); ip=Path(c["incident_path"])
        if sha_file(ip)!=c["incident_sha256"]: raise RuntimeError("incident digest mismatch")
        rmp=repl/"REPLACEMENT-ARMING-MANIFEST.json"
        if sha_file(rmp)!=c["replacement_arming_manifest_sha256"]: raise RuntimeError("replacement arming digest mismatch")
        verify_repo(); lock=acquire_lock()
        runner=REPO/"bench"/"R1"/"external-runner"/"r1_runner.py"
        bundle=repl/"external-bundle"/"r1-external"; state=repl/"state"; packages=repl/"packages"
        runroot=repl/"runs"/"variance-pilot"; preflight=repl/"preflight.json"; logs=repl/"supervisor-logs"
        runroot.mkdir(parents=True,exist_ok=True)
        cmd=[sys.executable,str(runner),"run","--bundle",str(bundle),"--repo-root",str(REPO),
             "--state-root",str(state),"--packages",str(packages),"--out",str(runroot),
             "--preflight-record",str(preflight),"--model","gpt-5.6-terra","--reasoning-effort","medium",
             "--seed",SEED,"--repeats","4","--trajectories","2","--max-output","1024"]
        so,se=logs/"runner-stdout.txt",logs/"runner-stderr.txt"
        rc=run_cmd(cmd,REPO,so,se,os.environ.copy())
        os.environ.pop("OPENAI_API_KEY",None)
        sout=so.read_text(encoding="utf-8",errors="replace") if so.exists() else ""
        serr=se.read_text(encoding="utf-8",errors="replace") if se.exists() else ""
        a=audit(runroot)
        base=["=== FEHREST R1-X1 REPLACEMENT VARIANCE PILOT REPORT ===",
              f"INCIDENT_SHA256={c['incident_sha256']}","INVALIDATED_SOURCE_BATCH=variance-pilot-599054280a96",
              f"REPLACEMENT_ROOT={repl}",f"RUNNER_EXIT_CODE={rc}",
              f"TRANSPORT_ATTEMPT_RECORDS={a['record_count']}",f"RAW_FILES={a['raw_count']}",
              f"EXECUTION_ORDER_ENTRIES={a['order_entry_count']}",
              f"DUPLICATE_RECORD_IDS={len(a['duplicate_record_ids'])}",
              f"DUPLICATE_ORDER_IDS={len(a['duplicate_order_ids'])}",
              f"ORPHAN_RAW_COUNT={len(a['orphan_raw'])}",
              f"RECORD_MISSING_RAW_COUNT={len(a['record_missing_raw'])}",
              f"ORDER_WITHOUT_RECORD_COUNT={len(a['order_without_record'])}",
              f"RECORD_WITHOUT_ORDER_COUNT={len(a['record_without_order'])}",
              "MODEL_RETURNED_VALUES="+",".join(a["model_returned_values"])]
        if rc!=0:
            write_result(base+["R1_VARIANCE_PILOT_FINAL_STATUS=HALTED_OR_INCOMPLETE","RAW_SEAL_STATUS=NOT_PRESENT",
                "OPENAI_API_KEY_CLEARED_FROM_SUPERVISOR=YES","SCORING_STATUS=NOT_STARTED",
                "UNBLINDING_STATUS=NOT_STARTED","POWER_ANALYSIS_STATUS=NOT_PERFORMED",
                "CONFIRMATORY_STATUS=NOT_STARTED","NEXT_GATE=REVIEW_REPLACEMENT_RUNNER_FAILURE","",
                "--- RUNNER STDOUT TAIL ---",*sout.splitlines()[-120:],"","--- RUNNER STDERR TAIL ---",*serr.splitlines()[-120:]])
            return 1
        if any((a["duplicate_record_ids"],a["duplicate_order_ids"],a["orphan_raw"],a["record_missing_raw"],
                a["order_without_record"],a["record_without_order"])) or not (a["record_count"]==a["raw_count"]==a["order_entry_count"]):
            write_result(base+["R1_VARIANCE_PILOT_FINAL_STATUS=HALTED_EVIDENCE_INTEGRITY","RAW_SEAL_STATUS=NOT_PRESENT",
                "SCORING_STATUS=NOT_STARTED","UNBLINDING_STATUS=NOT_STARTED","CONFIRMATORY_STATUS=NOT_STARTED",
                "NEXT_GATE=REVIEW_REPLACEMENT_EVIDENCE_INTEGRITY"])
            return 1
        if a["model_returned_values"] not in ([],["gpt-5.6-terra"]):
            write_result(base+["R1_VARIANCE_PILOT_FINAL_STATUS=HALTED_MODEL_IDENTITY_DRIFT","RAW_SEAL_STATUS=NOT_PRESENT",
                "SCORING_STATUS=NOT_STARTED","UNBLINDING_STATUS=NOT_STARTED","CONFIRMATORY_STATUS=NOT_STARTED",
                "NEXT_GATE=REVIEW_MODEL_IDENTITY_DRIFT"])
            return 1
        k=kv(sout)
        if k.get("R1_VARIANCE_PILOT_STATUS")!="EXECUTION_COMPLETE_UNSCORED": raise RuntimeError("missing complete marker")
        if k.get("PLANNED_TOTAL_SESSIONS")!="888": raise RuntimeError("planned session count changed")
        scan_o,scan_e=logs/"scan-stdout.txt",logs/"scan-stderr.txt"
        if run_cmd([sys.executable,str(runner),"scan","--out",str(runroot)],REPO,scan_o,scan_e,os.environ.copy())!=0:
            write_result(base+["R1_VARIANCE_PILOT_FINAL_STATUS=HALTED_SECRET_SCAN","SECRET_SCAN=FAIL","RAW_SEAL_STATUS=NOT_PRESENT",
                "SCORING_STATUS=NOT_STARTED","UNBLINDING_STATUS=NOT_STARTED","CONFIRMATORY_STATUS=NOT_STARTED",
                "NEXT_GATE=REVIEW_SECRET_SCAN_FAILURE"])
            return 1
        s1o,s1e=logs/"seal1-stdout.txt",logs/"seal1-stderr.txt"
        if run_cmd([sys.executable,str(runner),"seal","--out",str(runroot)],REPO,s1o,s1e,os.environ.copy())!=0: raise RuntimeError("seal1 failed")
        h1=kv(s1o.read_text(encoding="utf-8",errors="replace")).get("R1_VARIANCE_PILOT_RAW_SHA256")
        if not h1: raise RuntimeError("seal1 sha missing")
        s2o,s2e=logs/"seal2-stdout.txt",logs/"seal2-stderr.txt"
        if run_cmd([sys.executable,str(runner),"seal","--out",str(runroot)],REPO,s2o,s2e,os.environ.copy())!=0: raise RuntimeError("seal2 failed")
        h2=kv(s2o.read_text(encoding="utf-8",errors="replace")).get("R1_VARIANCE_PILOT_RAW_SHA256")
        if h1!=h2: raise RuntimeError("seal not reproducible")
        archive=runroot.parent/"variance-pilot-raw.tar.gz"
        if not archive.is_file() or sha_file(archive)!=h1: raise RuntimeError("archive digest mismatch")
        write_result(base+["R1_VARIANCE_PILOT_FINAL_STATUS=EXECUTION_COMPLETE_UNSCORED_REPLACEMENT",
            "SOURCE_BATCH_DISPOSITION=INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE",
            "SECRET_SCAN=PASS","RAW_SEAL_STATUS=PASS","RAW_SEAL_REPRODUCIBILITY=PASS",
            f"R1_VARIANCE_PILOT_RAW_SHA256={h1}",f"OK_RECORDS={a['ok_records']}",
            f"TASK_FAILURE_RECORDS={a['task_failure_records']}",f"INFRA_FAILURE_RECORDS={a['infra_failure_records']}",
            "OPENAI_API_KEY_CLEARED_FROM_SUPERVISOR=YES","SCORING_STATUS=NOT_STARTED",
            "UNBLINDING_STATUS=NOT_STARTED","POWER_ANALYSIS_STATUS=NOT_PERFORMED",
            "CONFIRMATORY_STATUS=NOT_STARTED","NEXT_GATE=FOUNDER_REVIEW_BEFORE_BLINDED_SCORING"])
        return 0
    except Exception as e:
        os.environ.pop("OPENAI_API_KEY",None)
        write_result(["=== FEHREST R1-X1 REPLACEMENT VARIANCE PILOT FAILURE ===",
            f"FAILURE_REASON={type(e).__name__}: {e}","OPENAI_API_KEY_CLEARED_FROM_SUPERVISOR=YES",
            "SCORING_STATUS=NOT_STARTED","UNBLINDING_STATUS=NOT_STARTED","CONFIRMATORY_STATUS=NOT_STARTED",
            "NEXT_GATE=REVIEW_REPLACEMENT_SUPERVISOR_FAILURE"])
        return 1
    finally:
        os.environ.pop("OPENAI_API_KEY",None)
        if lock is not None:
            try:
                import msvcrt; lock.seek(0); msvcrt.locking(lock.fileno(),msvcrt.LK_UNLCK,1)
            except Exception: pass
            try: lock.close()
            except Exception: pass

if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1] not in ("prepare","run"): raise SystemExit(2)
    raise SystemExit(prepare() if sys.argv[1]=="prepare" else run())
