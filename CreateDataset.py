import csv
import argparse
import os
import random
import faker

def generate_dataset():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_csv', help='Input wine dataset with no header.', required=True)
    parser.add_argument('--output_csv', help='Output transaction dataset.', default='output_dataset.csv')
    parser.add_argument('--num_wines', help='The number of wines that are available to transact.', type=int, required=True)
    parser.add_argument('--num_transactions', help='The total number of transactions to include in the dataset.', type=int, required=True)
    parser.add_argument('--num_users', help='The number of users to include in the dataset.', type=int, required=True)
    parser.add_argument('--avg_wines_purchased', help='The average number of wines purchased by any user.', type=int, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.input_csv):
        raise IOError("CSV file does not exist")

    if args.avg_wines_purchased >= args.num_wines:
        raise Exception("The average number of wines purchased should be less than the total number of wines")
    

    # Import the specified number of wines
    wine_list = []
    with open(args.input_csv, 'r') as in_csv_fh:
        reader = csv.reader(in_csv_fh)
        count = 0
        for row in reader:
            wine = divide_csv_wine_line(row)
            wine_list.append(wine)
            count += 1
            if count == args.num_wines:
                break
    
    user_list = gen_user_list(args.num_users)


    num_transactions = 0
    with open(args.output_csv, 'w', newline='') as out_csv_fh:
        writer = csv.writer(out_csv_fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(gen_csv_header())
        while num_transactions < args.num_transactions:
            user = choose_rand_user(user_list)
            num_purchased = how_many_wines_purchased(args.num_wines, args.avg_wines_purchased)
            wine_list_purchased = gen_random_wine_list(wine_list, num_purchased)
            rand_date_iso = gen_random_date_time()
            for wine in wine_list_purchased:
                csv_list = create_csv_list(user, wine, rand_date_iso)
                writer.writerow(csv_list)

            num_transactions += num_purchased

def choose_rand_user(user_list):
    index = random.randint(0, len(user_list) - 1)
    return user_list[index]

def gen_user_list(num_users):
    user_list = []
    for _ in range(1, num_users):
        #user_list.append(generate_username())
        fake = faker.Faker()
        rand_name = fake.name()
        rand_user = rand_name.replace(" ", "")
        user_list.append(rand_user)
    return user_list

def create_csv_list(user, wine, date_time):
    csv_list = [value for key, value in wine.items()]
    csv_list.append(user)
    csv_list.append(date_time)
    return csv_list

def gen_random_date_time():
    fake = faker.Faker()
    rand_date = fake.date_time()
    rand_date_iso = rand_date.isoformat()
    return rand_date_iso

def gen_random_wine_list(wine_list, num_purchased):
    # if num_purchased >= 2:
    #     print("Here")
    purchased_wine_list = []
    for _ in range(0, num_purchased):
        wine_index = random.randint(0, len(wine_list) - 1)
        wine = wine_list[wine_index]
        purchased_wine_list.append(wine)

    # find duplicate wines and increase their quantity
    unique_wine_list = [] 
    for purchased_wine in purchased_wine_list:
        duplicate = False
        for unique_wine in unique_wine_list:
            if unique_wine['index'] == purchased_wine['index']:
                unique_wine['quantity'] += 1
                duplicate = True
                break
        if not duplicate:
            unique_wine_list.append(purchased_wine)

    return unique_wine_list

def how_many_wines_purchased(num_wines, avg_wines_purchased):
    probability = avg_wines_purchased / num_wines
    list_purchased = [biased_filp(probability) for i in range(1, num_wines)]
    num_purchased = list_purchased.count(True)
    return num_purchased

def biased_filp(probability):
    if random.random() < probability: 
        return True 
    else:
        return False

def gen_csv_header():
    return [
        "Index", 
        "Country", 
        "Description", 
        "Designation",
        "Points",
        "Price",
        "Province",
        "Region_1",
        "Region_2",
        "Variety",
        "Winery",
        "Quantity",
        "User",
        "DateTime"
        ]

def divide_csv_wine_line(row):
    wine = {
        "index" : row[0],
        "country" : row[1],
        "description" : row[2],
        "designation" : row[3],
        "points" : row[4],
        "price" : row[5],
        "province" : row[6],
        "region_1" : row[7],
        "region_2" : row[8],
        "variety" : row[9],
        "winery" : row[10],
        "quantity" : 1
    }
    return wine

if __name__ == "__main__":
    generate_dataset()