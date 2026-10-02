#!/usr/bin/env python3
"""Local structured-input helper. Semantic judgments must be supplied or reviewed by a human/agent."""
import argparse, json, sys, math
from pathlib import Path
from datetime import date

def need(condition, message):
    if not condition: raise ValueError(message)
def ids(rows, label):
    seen=set()
    for row in rows:
        value=row.get('id'); need(isinstance(value,str) and value.strip(),label+' requires nonempty id')
        need(value not in seen,label+' duplicate id: '+value);seen.add(value)
    return seen
def number(value, label):
    need(not isinstance(value,bool) and isinstance(value,(int,float)) and math.isfinite(value),label+' must be finite number');return value

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        need(not args.output.exists(),'refusing to overwrite output')
        data=json.loads(args.input.read_text(encoding='utf-8'));need(isinstance(data,dict),'input must be object')
        result=process(data)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
        print(json.dumps({'output':str(args.output),'status':result.get('status','completed')},ensure_ascii=False))
        return 0 if result.get('status') not in ('blocked','failed') else 2
    except (ValueError,KeyError,TypeError,OSError) as e: print('error: '+str(e),file=sys.stderr);return 2

def process(d):
    evidence=ids(d['evidence'],'evidence');tasks=d['tasks'];need(tasks,'tasks required');ids(tasks,'tasks');gaps=[];rows=[]
    for task in tasks:
        for key in ('user','channel','trigger','priority','ai_boundary','human_handoff','acceptance','evidence_ids'): need(task.get(key),'task missing '+key)
        need(set(task['evidence_ids'])<=evidence,'unlinked requirement evidence')
        need(task['priority'] in ('must','should','could','out'),'invalid priority')
        if not task.get('acceptance_owner'): gaps.append(task['id']+': acceptance owner unknown')
        if task.get('requires_live_price') and task.get('ai_boundary')!='clarify_then_human_quote': gaps.append(task['id']+': live quote boundary unsafe')
        rows.append(task)
    for key in ('budget','volume','privacy_retention','support_hours','handoff_owner'): 
        if d.get(key) is None: gaps.append(key+': unknown; do not promise cost or SLA')
    return {'status':'draft_requires_clarification' if gaps else 'ready_for_acceptance_review','tasks':rows,'unknowns':gaps,'not_in_scope':d.get('not_in_scope',[]),'next_gate':'Confirm scope, acceptance owner and measured load before contracting.'}

if __name__ == "__main__": raise SystemExit(main())
