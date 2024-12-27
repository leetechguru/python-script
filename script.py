import csv
import re

def extract_data(file_path, datacenter, prefix):
    data = []
    with open(file_path, 'r') as file:
        content = file.read()
        # Match the required HTML pattern
        matches = re.finditer(
            r"<td>\s*<img.*?>\s*<a href='([^']+)'>((\d{5})_([a-zA-Z0-9_]+)_([tsTS]\d{2,6})_.*?)</a>\s*</td>",
            content
        )
        for match in matches:
            link_suffix = match.group(1)
            full_string = match.group(2)
            site_id = match.group(3)
            location_name = match.group(4)
            terminal = match.group(5)
            link = prefix + link_suffix

            data.append([datacenter, location_name, site_id, terminal, link])
    return data

def write_to_csv(data, output_file):
    headers = ["Datacenter", "Location name", "Site ID", "Terminal", "Link Description"]
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    at_file = "at.html"
    mi_file = "mi.html"
    at_prefix = "https://at-orionpoll01.corp.securustech.net"
    mi_prefix = "https://mi-orionpoll01.corp.securustech.net"
    
    at_data = extract_data(at_file, "at", at_prefix)
    mi_data = extract_data(mi_file, "mi", mi_prefix)
    
    
    combined_data = at_data + mi_data
    write_to_csv(combined_data, "TerminalsOrion.csv")

if __name__ == "__main__":
    main()
