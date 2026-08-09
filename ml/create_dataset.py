import random
import pandas as pd

random.seed(42)

data = []

for _ in range(1000):

    # Generate realistic environmental conditions
    temperature = round(random.uniform(18, 35), 1)
    humidity = round(random.uniform(40, 90), 1)

    # Soil sensor raw value
    # Higher value = drier condition
    soil_moisture = random.randint(700, 1024)

    # Prototype irrigation rule
    #
    # Very dry soil -> water needed
    # Moderately dry soil -> consider temperature/humidity
    # Wet soil -> no water needed

    if soil_moisture >= 950:
        water_needed = 1

    elif soil_moisture >= 850:
        if temperature >= 28 or humidity <= 55:
            water_needed = 1
        else:
            water_needed = 0

    else:
        water_needed = 0

    data.append([
        temperature,
        humidity,
        soil_moisture,
        water_needed
    ])


# Create DataFrame
df = pd.DataFrame(
    data,
    columns=[
        "temperature",
        "humidity",
        "soil_moisture",
        "water_needed"
    ]
)


# Save dataset
output_path = "dataset/irrigation_dataset.csv"

df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print()
print("Shape:", df.shape)
print()
print(df.head(10))
print()
print("Class distribution:")
print(df["water_needed"].value_counts())