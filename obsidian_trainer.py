import re
import os
import time
from openai import OpenAI
client = OpenAI()
# Example usage:
file_path = '/home/matt/Documents/obsidian_bubble_vault/bubble_trainer/your_file.md'
directory_path = '/home/matt/Documents/obsidian_bubble_vault/bubble_trainer/'
save_path = '/home/matt/Documents/obsidian_bubble_vault/Flashcards'

def save_mindmap():
    userdir = input("Save mindmap as?\n")
    flashcardpath = os.path.dirname(save_path)

    # Construct the full path for the new directory
    new_directory_path = os.path.join(save_path, userdir)

    # Create the new directory if it doesn't exist
    os.makedirs(new_directory_path, exist_ok=True)

    # Move all Markdown files from the current directory to the new directory
    os.system(f'mv {directory_path}/*.md {new_directory_path}')

def delete_mindmap():
    global directory_path
    try:
        os.system(f'rm {directory_path}/*.md')
        print("Markdown files removed successfully.")
    except Exception as e:
        print(f"Error: {e}")

def training_mode():
    global file_path

    def parse_markdown(file_path):

        if(file_path ==  '/home/matt/Documents/obsidian_bubble_vault/bubble_trainer/your_file.md'):
            print("Use option 2 to select a root node.")
            return

        # Define a dictionary to store replaced text
        references = {}

        # Read the Markdown file using an absolute path
        with open(file_path, 'r') as file:
            markdown_content = file.read()

        # Define the regex pattern to find text between double brackets
        pattern = r'\[\[(.*?)\]\]'

        # Use regex to replace text surrounded by double brackets with increasing question marks
        def replace_text(match):
            text_to_replace = match.group(1)
            references[len(references)] = text_to_replace
            question_marks = '?' * (len(references))  # Append two extra question marks for each replacement
            return f'[[{question_marks}]]'

        replaced_content = re.sub(pattern, replace_text, markdown_content)

        # Write the modified content back to the original file
        with open(file_path, 'w') as file:
            file.write(replaced_content)

        # Check other markdown files in the parent directory
        parent_directory_path = os.path.dirname(file_path)

        for filename in os.listdir(parent_directory_path):
            if filename.endswith('.md') and filename != os.path.basename(file_path):
                original_filename = os.path.splitext(filename)[0]

                # Check if the file name is a reference
                if original_filename in references.values():
                    position = list(references.values()).index(original_filename)
                    associated_string = '?' * (position + 1)
                    new_file_path = os.path.join(parent_directory_path, associated_string + '.md')
                    os.rename(os.path.join(parent_directory_path, filename), new_file_path)

        start_time = time.time()

        # Prompt the user to resolve references
        skipped_indices = list(range(len(references)))

        while skipped_indices:
            user_input = input(f"\nEnter a node (or 'q' to exit): ").lower()

            # Check if user wants to exit
            if user_input == 'q':
                break

            # Check if user input is correct
            if user_input in references.values():
                print("\nCorrect!")

                # Find the index of the reference
                index = list(references.values()).index(user_input)

                # Write back the correct value to the Markdown file
                replaced_content = replaced_content.replace(f'[[{"?" * (index + 1)}]]', f'[[{user_input}]]', 1)
                with open(file_path, 'w') as file:
                    file.write(replaced_content)

                # Remove the index from skipped_indices since the user got it correct
                skipped_indices.remove(index)

                # Rename the file back to the correct value for skipped indices
                restored_filename = os.path.join(parent_directory_path, references[index] + '.md')
                new_file_path = os.path.join(parent_directory_path, '?' * (index + 1) + '.md')
                os.rename(new_file_path, restored_filename)
            else:
                    skipped_index = skipped_indices[0] if skipped_indices else None
                    chosen_topic = references[skipped_index]

                    user_message = f"tell me about {chosen_topic} without explicitly saying it by name"

                    response = client.chat.completions.create(
                      model="gpt-3.5-turbo",
                      messages=[
                        {"role": "assistant", "content": "I am a student using this application for hints on topics and i am trying to use active recall to consolidate retention of these topics. I want you to tell me about the topics i describe to you without explicitly telling me what they are. I will be telling you the topics but you should not repeat them by name to me. it is my responsibility to recall them and it is important you do not mention them by name."},
                        {"role": "user", "content": user_message}
                      ]
                    )

                    response_message = response.choices[0].message.content
                    chosen_topicUpperC = chosen_topic[0].upper() + chosen_topic[1:]

                    if chosen_topic in response_message:
                        # Replace chosen_topic with question marks using regular expressions
                        response_message = re.sub(chosen_topic, '?' * len(chosen_topic), response_message)
                    if chosen_topicUpperC in response_message:
                            # Replace chosen_topic with question marks using regular expressions
                        response_message = re.sub(chosen_topicUpperC, '?' * len(chosen_topic),response_message)

                    print(response_message)

        for skipped_index in skipped_indices:
            user_input = references[skipped_index].lower()

            # Write back the correct value to the Markdown file
            replaced_content = replaced_content.replace(f'[[{"?" * (skipped_index + 1)}]]', f'[[{user_input}]]', 1)

            with open(file_path, 'w') as file:
                file.write(replaced_content)

            # Rename the file back to the correct value for skipped indices
            restored_filename = os.path.join(parent_directory_path, user_input + '.md')
            new_file_path = os.path.join(parent_directory_path, '?' * (skipped_index + 1) + '.md')
            os.rename(new_file_path, restored_filename)

        # Display statistics
        end_time = time.time()
        elapsed_time = end_time - start_time
        retention_rate = (len(references) - len(skipped_indices)) / len(references) if len(references) != 0 else 0

        print(f"\nTime taken to finish: {elapsed_time:.2f} seconds")
        print(f"Retention rate: {retention_rate * 100:.2f}% (Correct: {len(references) - len(skipped_indices)}/{len(references)})")

    parse_markdown(file_path)


def select_root_node():
    global file_path  # Use the global file_path variable
    new_filename = input("Enter the new filename (without extension): ")
    # Extract the directory path from the global file_path
    directory_path = os.path.dirname(file_path)
    # Modify the file path with the new filename
    file_path = os.path.join(directory_path, f'{new_filename}.md')

# accessory functions for generate_mindmap

def create_markdown_file(filename):
    with open(filename, 'w') as file:
        file.write('---\n')

def append_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(f'[[{content}]]\n')

def generate_mindmap():
    global directory_path, file_path
    try:
        root_node = input("Enter Root Node: ")
        root_filename = f'{root_node}.md'
        create_markdown_file(root_filename)

        first_level_dependencies = input("Enter First Level Dependencies (separate with commas): ").split(',')
        for dependency in first_level_dependencies:
            dep_filename = f'{dependency.strip()}.md'
            create_markdown_file(dep_filename)
            append_to_file(root_filename, dependency.strip())

        # Prompt to continue with first level dependencies
        continue_first_level = input("Do you want to continue with first level dependencies? (Y/N): ").lower()
        if continue_first_level != 'y':
            print("Exiting.")

            new_filename = root_node
            # Extract the directory path from the global file_path
            directory_path = os.path.dirname(file_path)
            # Modify the file path with the new filename
            file_path = os.path.join(directory_path, f'{new_filename}.md')

            return

        try:
            second_level_dependencies = []
            for node in first_level_dependencies:
                node_filename = f'{node.strip()}.md'
                create_markdown_file(node_filename)

                second_level_nodes = input(f"Enter Dependencies for {node.strip()} (separate with commas): ").split(',')
                for second_node in second_level_nodes:
                    second_node_filename = f'{second_node.strip()}.md'
                    create_markdown_file(second_node_filename)
                    append_to_file(node_filename, second_node.strip())
                    second_level_dependencies.append(second_node.strip())

            continue_second_level = input("Do you want to continue with second level dependencies? (Y/N): ").lower()
            while continue_second_level == 'y':
                new_second_level_dependencies = []
                for node in second_level_dependencies:
                    add_node = input(f"Do you want to add nodes for {node.strip()}? (Y/N): ").lower()
                    if add_node == 'y':
                        node_filename = f'{node.strip()}.md'
                        new_second_nodes = input(f"Enter Dependencies for {node.strip()} (separate with commas): ").split(',')
                        for new_second_node in new_second_nodes:
                            new_second_node_filename = f'{new_second_node.strip()}.md'
                            create_markdown_file(new_second_node_filename)
                            append_to_file(node_filename, new_second_node.strip())
                            new_second_level_dependencies.append(new_second_node.strip())

                second_level_dependencies = new_second_level_dependencies
                continue_second_level = input("Do you want to continue with second level dependencies? (Y/N): ").lower()

        except KeyboardInterrupt:
            print("\nTerminated by user. Cleaning up and exiting.")
            return

    except KeyboardInterrupt:
        print("\nTerminated by user. Cleaning up and exiting.")
        return

    new_filename = root_node
    # Extract the directory path from the global file_path
    directory_path = os.path.dirname(file_path)
    # Modify the file path with the new filename
    file_path = os.path.join(directory_path, f'{new_filename}.md')

    print("Exiting.")

def exit_program():
    print("Exiting program")
    # Add any cleanup logic here if needed
    exit()

# Define a dictionary mapping choices to functions
menu_options = {
    "1": training_mode,
    "2": select_root_node,
    "3": generate_mindmap,
    "4": delete_mindmap,
    "5": save_mindmap,
    "6": exit_program,
}

while True:
    print("\nMenu:")
    for key, value in menu_options.items():
        print(f"{key}. {value.__name__.replace('_', ' ').title()}")  # Format function names

    choice = input("\nEnter your choice (1-6): ")

    # Use the dictionary to call the corresponding function
    menu_options.get(choice, lambda: print("Invalid choice"))()
