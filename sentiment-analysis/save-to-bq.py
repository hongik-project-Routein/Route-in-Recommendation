from google.cloud import bigquery
client = bigquery.Client()

table_id = "carbon-inkwell-290604.route_in.sentimental_score"

def save_sa(row_list):
    for row in row_list:
        userId = row[0]
        mapId = row[1]
        score = row[2]

        rows_to_insert = [
        {"userId": userId, "mapId": mapId, "score": score}
        ]

        errors = client.insert_rows_json(
            table_id, rows_to_insert
        )  # Make an API request.
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))

    return "Complete def save_sa"
