def print_report(job_id, res):
    print("\n ╔" + "═" * 70 + "╗")
    print(f" ║ JOB {job_id} DIAGNOSIS{' ' * 50}║")
    print(" ╠" + "═" * 70 + "╣")
    print(f" ║ WHAT: {res['what']:<60}║")
    print(f" ║ WHY : {res['why']:<60}║")
    print(f" ║ FIX : {res['fix']:<60}║")
    print(" ╚" + "═" * 70 + "╝")