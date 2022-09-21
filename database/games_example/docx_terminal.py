import csv, sys

# python modify.py football.py out.py

argc = len(sys.argv)
argv = sys.argv 

def modify(filename, new_filename, prize):
    temp = open(new_filename, "w")

    with open(filename) as open_file:
        prize = ""
        # this filters out newlines in 
        filter = (line.replace("\n", '') for line in open_file)
        for index, row in enumerate(csv.reader(filter)):
            for i in range(len(row)):
                if index == 0:
                    if i == 0:
                        prize = row[i]
                        row[i] = "Name"
                    elif i < len(row) - 1:
                        row[i] = "E" + str(i)
                    else:
                        row[i] = "PTS"

                if i == len(row) - 1:
                    temp.write(row[i])
                else:
                    temp.write(row[i]+",")
            temp.write("\n")
        temp.close()
        open_file.close()
        return prize.split("$")[1]


def passed():
    if argc != 3:
        print("Usage: python modify.py original.csv out.csv")
        return False
    return True


def main():
    prize = ""
    if passed:
        week2 = modify(argv[1], argv[2], prize)

    print(f"Prize amount is: ${week2}")
    
    
main()






