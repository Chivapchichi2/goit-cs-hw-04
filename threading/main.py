import threading

def search_files(files, keywords, results):
    found_files = {}
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    if keyword not in found_files:
                        found_files[keyword] = []
                    found_files[keyword].append(file)
    results.append(found_files)

def main():
    files = ['../file1.txt', '../file2.txt', '../file3.txt']
    keywords = ['exercise', 'forest', 'chocolate cake']
    num_threads = 3

    thread_results = []
    threads = []

    chunk_size = len(files) // num_threads
    file_chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    for chunk in file_chunks:
        thread = threading.Thread(target=search_files, args=(chunk, keywords, thread_results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    final_results = {}
    for result in thread_results:
        for key, value in result.items():
            if key not in final_results:
                final_results[key] = []
            final_results[key].extend(value)

    print(final_results)

if __name__ == "__main__":
    main()
