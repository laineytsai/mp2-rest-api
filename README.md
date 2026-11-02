# MP2: Data Processing REST API

This project is a FastAPI application that lets clients upload, process, 
and retrieve CSV data through a REST API. A CSV can be uploaded with 
`POST /upload`, which is validated and stored with a unique dataset ID. 
The client can then send processing settings as JSON to `POST /datasets/{dataset_id}/process`, 
which reuses the MP1 pipeline modules in `data_pipeline/` to validate the data, 
remove duplicates, handle missing values, and remove outliers, returning 
a cleaning report. The processed data can be retrieved with `GET /datasets/{dataset_id}`, 
and `GET /health` reports the application's status. Request and response data are 
validated with Pydantic models, and middleware logs every request with a unique request ID, 
status code, and duration. Errors return status codes, such as 400 for invalid uploads 
or settings and 404 for missing datasets.

## Running the API

```bash
python -m uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs to try the endpoints.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Returns the application status and version |
| POST | `/upload` | Uploads and stores a CSV file, returning its metadata |
| GET | `/datasets/{dataset_id}` | Returns up to `limit` rows of a stored dataset |
| POST | `/datasets/{dataset_id}/process` | Validates and cleans a stored dataset using MP1 functions |

## Running the Tests

```bash
python -m pytest tests -v
```