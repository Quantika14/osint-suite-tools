from intelxapi import intelx
import modules.key as KEY

intelx = intelx(KEY.intelx)

def get_pastes(target):
    results = intelx.search(target, buckets=['pastes'], maxresults=2000)
    record_count = len(results['records'])
    print(f"|----[INFO][>] Found {record_count} records for {target} in bucket 'pastes'")

    if record_count > 0:
        print("|----[INFO][>] Downloading paste in file.txt...")
        intelx.FILE_READ(results['records'][0]['systemid'], 0, results['records'][0]['bucket'], "file.txt")

def get_leaks(target):
    results = intelx.search(target, buckets=['leaks.public','leaks.private'], maxresults=2000)
    record_count = len(results['records'])
    print(f"|----[INFO][>] Found {record_count} records for {target} in bucket 'leaks'")

    if record_count > 0:
        print("|----[INFO][>] Downloading leak in file.txt...")
        intelx.FILE_READ(results['records'][0]['systemid'], 0, results['records'][0]['bucket'], "file.txt")

def get_darknet(target):
    results = intelx.search(target, buckets=['darknet'], maxresults=2000)
    record_count = len(results['records'])
    print(f"|----[INFO][>] Found {record_count} records for {target} in bucket 'darknet'")

    if record_count > 0:
        print("|----[INFO][>] Downloading link in darknet in file.txt...")
        intelx.FILE_READ(results['records'][0]['systemid'], 0, results['records'][0]['bucket'], "file.txt")

