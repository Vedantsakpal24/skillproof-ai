import threading
import subprocess
import json
import sqlite3
import re

class TimeoutError(Exception):
    pass

def execute_code(skill_name: str, code: str, test_cases: list) -> dict:
    skill = skill_name.lower()
    
    if skill == "python":
        return execute_python(code, test_cases)
    elif skill in ["javascript", "node.js"]:
        return execute_javascript(code, test_cases)
    elif skill == "sql":
        return execute_sql(code, test_cases)
    else:
        # Fallback for HTML, CSS, React, Docker - simple keyword matching
        return execute_keyword_match(code, test_cases)

def execute_python(code: str, test_cases: list) -> dict:
    results = {"passed": 0, "failed": 0, "total": len(test_cases), "details": []}
    
    safe_globals = {
        "__builtins__": {
            "print": print, "range": range, "len": len, "list": list, "dict": dict,
            "set": set, "tuple": tuple, "int": int, "float": float, "str": str,
            "bool": bool, "sum": sum, "max": max, "min": min, "abs": abs,
            "enumerate": enumerate, "zip": zip
        }
    }
    
    for tc in test_cases:
        test_code = f"{code}\n\nresult = {tc['call']}"
        local_env = {}
        
        try:
            def run_test():
                exec(test_code, safe_globals, local_env)
                
            thread = threading.Thread(target=run_test)
            thread.start()
            thread.join(timeout=2.0)
            
            if thread.is_alive():
                raise TimeoutError("Execution timed out")
                
            actual = local_env.get("result")
            if actual == tc["expected"]:
                results["passed"] += 1
                results["details"].append({"call": tc["call"], "status": "pass"})
            else:
                results["failed"] += 1
                results["details"].append({"call": tc["call"], "status": "fail", "expected": tc["expected"], "actual": actual})
        except Exception as e:
            results["failed"] += 1
            results["details"].append({"call": tc["call"], "status": "error", "error": str(e)})
            
    return results

def execute_javascript(code: str, test_cases: list) -> dict:
    results = {"passed": 0, "failed": 0, "total": len(test_cases), "details": []}
    
    for tc in test_cases:
        # Wrap the code and the test call, print the result to stdout
        js_code = f"{code}\nconsole.log(JSON.stringify({tc['call']}));"
        
        try:
            process = subprocess.Popen(['node', '-e', js_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=2.0)
            
            if process.returncode != 0:
                results["failed"] += 1
                results["details"].append({"call": tc["call"], "status": "error", "error": stderr.strip()})
                continue
                
            try:
                actual = json.loads(stdout.strip())
            except json.JSONDecodeError:
                actual = stdout.strip()
                
            if actual == tc["expected"]:
                results["passed"] += 1
                results["details"].append({"call": tc["call"], "status": "pass"})
            else:
                results["failed"] += 1
                results["details"].append({"call": tc["call"], "status": "fail", "expected": tc["expected"], "actual": actual})
                
        except subprocess.TimeoutExpired:
            process.kill()
            results["failed"] += 1
            results["details"].append({"call": tc["call"], "status": "error", "error": "Execution timed out"})
        except Exception as e:
            results["failed"] += 1
            results["details"].append({"call": tc["call"], "status": "error", "error": str(e)})
            
    return results

def execute_sql(code: str, test_cases: list) -> dict:
    results = {"passed": 0, "failed": 0, "total": len(test_cases), "details": []}
    
    for tc in test_cases:
        try:
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            
            # Setup dummy table if defined in test case
            if "setup" in tc:
                cursor.executescript(tc["setup"])
                
            # Run user query
            cursor.execute(code)
            actual = cursor.fetchall()
            
            if actual == tc["expected"]:
                results["passed"] += 1
                results["details"].append({"call": tc.get("description", "SQL Query"), "status": "pass"})
            else:
                results["failed"] += 1
                results["details"].append({"call": tc.get("description", "SQL Query"), "status": "fail", "expected": tc["expected"], "actual": actual})
                
            conn.close()
        except Exception as e:
            results["failed"] += 1
            results["details"].append({"call": tc.get("description", "SQL Query"), "status": "error", "error": str(e)})
            
    return results

def execute_keyword_match(code: str, test_cases: list) -> dict:
    results = {"passed": 0, "failed": 0, "total": len(test_cases), "details": []}
    
    code_lower = code.lower()
    for tc in test_cases:
        required_keywords = tc["expected"]
        passed = all(kw.lower() in code_lower for kw in required_keywords)
        
        if passed:
            results["passed"] += 1
            results["details"].append({"call": tc.get("description", "Syntax Check"), "status": "pass"})
        else:
            results["failed"] += 1
            results["details"].append({"call": tc.get("description", "Syntax Check"), "status": "fail", "expected": required_keywords, "actual": "Missing keywords"})
            
    return results
