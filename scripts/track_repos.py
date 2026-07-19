#!/usr/bin/env python3
import json
import subprocess
import sys

OWNER = "jomellikesturtles"
REPOS = [
    "mdb-admin-web-app",
    "mdb-overview",
    "mdb-electron",
    "mdb-api",
    "mdb-admin-bff-service",
    "user-data-gateway-service",
    "media-data-gateway-service",
    "mdb-cli",
    "mdb-platform",
    "notification-service",
    "aiops-remediation-service",
    "mdb-crawler-service"
]

def run_gh_api(endpoint):
    try:
        result = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        # If it's a 404 or access error, return None
        return None
    except json.JSONDecodeError:
        return None

def check_branch_protection(repo, branch):
    # Check if protection endpoint returns 200
    res = run_gh_api(f"repos/{OWNER}/{repo}/branches/{branch}/protection")
    if res is not None:
        return True, "Protected"
    
    # Check if branch exists at all
    branch_info = run_gh_api(f"repos/{OWNER}/{repo}/branches/{branch}")
    if branch_info is None:
        return False, "N/A"
    return False, "Unprotected"

def check_cicd_status(repo, branch):
    # Fetch workflows
    workflows_data = run_gh_api(f"repos/{OWNER}/{repo}/actions/workflows")
    if not workflows_data or workflows_data.get("total_count", 0) == 0:
        return "No Workflows"
    
    # Fetch latest runs for this branch
    runs_data = run_gh_api(f"repos/{OWNER}/{repo}/actions/runs?branch={branch}&per_page=10")
    if not runs_data or runs_data.get("total_count", 0) == 0:
        return "No Runs"
    
    runs = runs_data.get("workflow_runs", [])
    pr_ok = False
    merge_ok = False
    
    for r in runs:
        event = r.get("event")
        conclusion = r.get("conclusion")
        status = r.get("status")
        
        # We look for completed runs
        if status == "completed":
            if event == "pull_request" and conclusion == "success":
                pr_ok = True
            elif event == "push" and conclusion == "success":
                merge_ok = True
                
    if pr_ok and merge_ok:
        return "✅ PR & Merge Pass"
    elif pr_ok:
        return "⚠️ PR Pass Only"
    elif merge_ok:
        return "⚠️ Merge Pass Only"
    else:
        # Check if there are active configurations
        return "❌ Runs Failed / None Succeeded"

def main():
    print("Gathering repository metadata from GitHub via 'gh' CLI...")
    print(f"Target Owner: {OWNER}")
    print("-" * 60)
    
    # Markdown Table Header
    report = []
    report.append(f"# Repository Status Report ({OWNER})")
    report.append(f"Generated via `track_repos.py` script using local GitHub CLI validation.\n")
    report.append("| Repository | Visibility | Master Branch Protection | CI/CD Status (master) | Default Branch |")
    report.append("| :--- | :--- | :--- | :--- | :--- |")
    
    for repo in REPOS:
        sys.stdout.write(f"Analyzing {repo}... ")
        sys.stdout.flush()
        
        repo_data = run_gh_api(f"repos/{OWNER}/{repo}")
        if not repo_data:
            print("❌ Access Denied / Not Found")
            report.append(f"| {repo} | Unknown / Private | Unknown | Unknown | Unknown |")
            continue
            
        visibility = repo_data.get("visibility", "unknown").capitalize()
        default_branch = repo_data.get("default_branch", "master")
        
        # Check protection on default branch (and master if default is main)
        has_protection, prot_label = check_branch_protection(repo, "master")
        if prot_label == "N/A" and default_branch != "master":
            # Check default branch instead
            has_protection, prot_label = check_branch_protection(repo, default_branch)
            target_branch = default_branch
        else:
            target_branch = "master"
            
        cicd_status = check_cicd_status(repo, target_branch)
        
        print("✅ Done")
        report.append(f"| `{repo}` | {visibility} | {prot_label} ({target_branch}) | {cicd_status} | `{default_branch}` |")
        
    # Write report to file
    report_content = "\n".join(report)
    with open("repo_status_report.md", "w") as f:
        f.write(report_content)
        
    print("\nReport written to 'repo_status_report.md'.")
    print("\n" + report_content)

if __name__ == "__main__":
    main()
