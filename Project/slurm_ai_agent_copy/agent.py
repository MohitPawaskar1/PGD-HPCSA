from rule_engine import analyze_job
from parser_engine import get_current_jobs, get_log_content, get_wait_time
from cloud_engine import check_cloud_need
from formatter import print_report
import time

def main():
    print("\n🚀 CDAC AI AGENT V21 | Modular Cluster Watchdog\n")

    processed = set()

    while True:
        try:
            jobs = get_current_jobs()

            for job in jobs:
                jid = job["id"]

                # Avoid duplicate processing
                if jid in processed:
                    continue

                # ----------------------------------------
                # CLOUD BURST CHECK (before anything else)
                # ----------------------------------------
                cloud_alert = check_cloud_need(job)
                if cloud_alert:
                    print(cloud_alert)
                    processed.add(jid)
                    continue

                # ----------------------------------------
                # FETCH LOG & WAIT TIME
                # ----------------------------------------
                log_text = get_log_content(jid)
                wait_minutes = get_wait_time(job["submit_time"])

                # ----------------------------------------
                # AI + RULE ENGINE ANALYSIS
                # ----------------------------------------
                result = analyze_job(
                    job,         # job dictionary from parser
                    log_text,    # extracted log
                    wait_minutes # pending minutes
                )

                # ----------------------------------------
                # PRINT FINAL REPORT
                # ----------------------------------------
                print_report(jid, result)

                processed.add(jid)

        except Exception as e:
            print(f"\n❌ Agent error: {e}")

        # Poll SLURM every 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    main()