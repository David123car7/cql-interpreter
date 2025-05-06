import csv

class Files:
    
    def read_csv(self, filename):
                if(filename == ""):
                    print("Filename is empty")
                    return None

                try:
                    data = []
                    header = None

                    with open(filename, "r", newline="") as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            if row and row[0].startswith("#"):
                                continue

                            # First line is the header
                            if header is None:
                                header = row
                            else:
                                data.append(row)
                    print(header)
                    print(data)
                    return {"header": header, "data": data}
                except Exception as e:
                    print(f"Error reading CSV file: {str(e)}")
                    return None
                
    def write_csv(self, filename, data):
         if filename == "":
            print("Filename is empty")
            return None
         
         try:
            with open(filename, mode= 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data["header"])
                for row in data["data"]:
                    writer.writerow(row)
         except Exception as e:
            print(f"Error writing CSV file: {str(e)}")
            return None
