import azure.functions as func
import json
import io
import os

from azure.storage.blob import BlobServiceClient

from data_analysis import analyze_diets


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:

        connection_string = os.environ["AzureWebJobsStorage"]

        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        blob_client = blob_service_client.get_blob_client(
            container="datasets",
            blob="All_Diets.csv"
        )

        csv_data = blob_client.download_blob().readall()

        result = analyze_diets(
            io.BytesIO(csv_data)
        )

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:

        return func.HttpResponse(
            json.dumps({
                "error": str(e)
            }),
            mimetype="application/json",
            status_code=500
        )