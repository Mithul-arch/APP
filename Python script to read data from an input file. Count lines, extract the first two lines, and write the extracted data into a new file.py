def count_lines(file_path):
    """Count the total number of lines in a file."""
    with open(file_path, "r") as f:
        return sum(1 for _ in f)

def extract_first_lines(file_path, num_lines=2):
    """Extract the first 'num_lines' lines from a file."""
    extracted = []
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if i >= num_lines:
                break
            extracted.append(line)
    return extracted

def write_lines(file_path, lines):
    """Write a list of lines to a new file."""
    with open(file_path, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"

    with open(input_file, "w") as f:
        f.write("Line 1: Monday\nLine 2: Tuesday\nLine 3: Wednesday\nLine 4: Thursday\nLine 5: Friday\n")

    total_lines = count_lines(input_file)
    print(f"Total lines in '{input_file}': {total_lines}")

    first_two_lines = extract_first_lines(input_file, num_lines=2)

    write_lines(output_file, first_two_lines)
    print(f"Successfully extracted first 2 lines to '{output_file}'.")