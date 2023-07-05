
from collections import Counter

data = []  # List to store the tuples
concatenated_words = ''  # Variable to store concatenated words

# Open the file
with open('C:\practica\summarizer\summarizer\Image_Detection\General_Info.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line into words
        words = line.strip().split()

        # Iterate over the words in the line
        for word in words:
            if word.isnumeric():# Check if the word is a number
                break# Break the loop if a number is encountered
            else:
                # Concatenate the word to the existing string
                concatenated_words += word + ' '

        print(concatenated_words)
        # Split the concatenated words into label and confidence
        split_values = concatenated_words.strip().split()
        if len(split_values) == 2:
            label, confidence = split_values[0], split_values[1]
            data.append((label, float(confidence)))

        # Reset the concatenated words variable
        concatenated_words = ''

# Convert the list of tuples to a tuple
data_tuple = tuple(data)

treshold = input("Enter a treshold for acceptable detected items: ")
my_list = []

for l in range(len(data_tuple)):
    if(float(data_tuple[l][1])>float(treshold)):
        my_list.append(data_tuple[l][0])

#counting the nr. of appearances of each element in the list
counter = Counter(my_list)

# Sorting the counter elements in descending order of count
sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)

file_path = input("Enter the file path of the final file: ")

with open(file_path +'\ObjectsInSequence.txt', 'w') as file:
    # Read each line in the file
    for element, count in sorted_counter:
        file.write(f"{element}: {count}")
        file.write("\n")

    # file.write("List containing only objects:")
    # for element, count in sorted_counter:
    #     if element== "person":
    #         break
    #     else:
    #        file.write(f"{element}: {count}")
    #        file.write("\n")













