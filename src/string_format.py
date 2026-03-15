def format_list_of_dictionary_to_string(list_of_dictionary):
    format_string = ""
    for entry in list_of_dictionary:
        if "content" in entry:
            format_string =  format_string  + entry['phase'] + " :\n"+ entry['content'] + "\n"
        elif "word-limit" in entry:
            format_string =  format_string  + entry['phase'] + " : "+ entry['word-limit'] + "\n"
    return format_string
