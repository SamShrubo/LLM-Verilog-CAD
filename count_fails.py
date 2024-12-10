with open('dedupe-test-512-2.txt', 'r', encoding='utf-8', errors='ignore') as fd:
    lines = fd.readlines()
    f_count =0
    s_count =0
    for line in lines:
        if line.find("Failed") != -1:
            count += 1
    print(f"Failed on {count} files")
    print(f"Failed on {count} files")
