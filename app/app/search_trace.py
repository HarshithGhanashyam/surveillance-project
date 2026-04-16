import csv

SIGHTINGS_FILE = "data/sightings.csv"


def search_by_roll_no(roll_no):
    results = []

    try:
        with open(SIGHTINGS_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["Roll No"].strip() == roll_no.strip():
                    results.append(row)

    except FileNotFoundError:
        print("[ERROR] sightings.csv not found")

    return results


if __name__ == "__main__":
    roll = input("Enter Roll Number to trace: ").strip()
    matches = search_by_roll_no(roll)

    if not matches:
        print("No detections found.")
    else:
        print(f"\nTrace results for {roll}:\n")
        for row in matches:
            print(
                f"{row['Name']} | {row['Roll No']} | {row['Camera ID']} | "
                f"{row['Date']} {row['Time']} | Score: {row['Score']}"
            )