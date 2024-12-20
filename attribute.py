
import os
import csv


def create_attribute_data(filename):

# Read the input CSV file
    with open(filename, 'r') as infile:
        reader = csv.DictReader(infile)
        data = [row for row in reader]
        print("Data read from input CSV file:")
    # print(data)
# Print the column names
# print("Column names:")
# print(reader.fieldnames)

# Process the data
    output_data = []
    for row in data:
    # print("Row data:")
    # print(row)
        for column in ['categories', 'sub_categories']:
            if column in row:
                if row[column] is not None and ';' in row[column]:
                    values = row[column].split(';')
                    for value in values:
                        output_data.append({
                            'customer_id': row['customer_id'],
                            'attributes': column,
                            'values': value.strip()
                        })
                else:
                    output_data.append({
                        'customer_id': row['customer_id'],
                        'attributes': column,
                        'values': row[column]
                    })

# Write the output CSV file
    with open('attribute.csv', 'w', newline='') as outfile:
            fieldnames = ['customer_id', 'attributes', 'values']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_data)
            print("Output CSV file written successfully.")
            return(len(output_data))

