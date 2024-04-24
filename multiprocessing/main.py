import multiprocessing
import time

def search_files(files, keywords, results):
    found_files = {}
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        if keyword not in found_files:
                            found_files[keyword] = []
                        found_files[keyword].append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    results.put(found_files)

def main():
    files = ['../file1.txt', '../file2.txt', '../file3.txt']
    keywords = ['exercise', 'forest', 'chocolate cake']
    num_processes = 3

    manager = multiprocessing.Manager()
    process_results = manager.Queue()
    processes = []
    start_time = time.time()

    chunk_size = len(files) // num_processes
    file_chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    for chunk in file_chunks:
        process = multiprocessing.Process(target=search_files, args=(chunk, keywords, process_results))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    final_results = {}
    while not process_results.empty():
        result = process_results.get()
        for key, value in result.items():
            if key not in final_results:
                final_results[key] = []
            final_results[key].extend(value)

    print("Multiprocessing results:", final_results)
    print("Time taken for multiprocessing:", time.time() - start_time)

if __name__ == "__main__":
    main()
