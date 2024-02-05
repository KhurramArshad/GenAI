def read_and_convert_to_dict(file_path):
    result_dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                print(line)
                key, value = line.split('=')
                result_dict[key.strip()] = value.strip()

    return result_dict

# Example usage
file_path = '../data/slang.txt'  # Replace with the actual path to your text file
result_dictionary = read_and_convert_to_dict(file_path)

print(result_dictionary)