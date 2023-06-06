--- 
title: Api endpoints
marp: true
---

# Login
- Login: `POST /api/login`
    - Params: Can take refresh=true to refresh the token and log the user in again. the `Token` cookie should be sent with the request.
    - Body: 
    ```ts
    {
        "username": string,
        "password": string
    }
    // or empty body if refresh=true
    ```
    - Response:
    adds 2 cookies to the response, one with the name `Token` that is http only and the value of the token. and one empty cookie with the name `Authenticated` to be used in the front end to verify that the user is logged in.
--- 
# Logout
`POST /api/logout` Does not require a body
- Response:
    removes the `Token` and `Authenticated` cookies from the response.
---

# Register
 `POST /api/register`
- Body:
```ts
{
    "username": string,
    "password": string,
    "email": string // no clue if we should keep it.
}
```
- Response: response code 201 `created` if the user was created successfully.

---

# Upload File

`POST /api/upload` used to upload a csv file to the server.
- Params: fileType can be either `internal` or `external` to specify the type of the file, this is useful to know in what db we should put the data. only accepts CSV files.
- Body: form data with the file to upload
- Response: response code 201 `created` if the file was uploaded successfully.
--- 
# Predictions: 

`GET /api/predictions` used to get predictions on either, revenue or profit on a range of dates.
- Params: `type` can be either `revenue` or `profit` to specify the type of the prediction.
- Body: 
```ts
{
    "dates": [
        string,
        string,
        ...
    ] // dates in the format of IsoString
}
```
---
- Response: response code 200 `ok` if the predictions were generated successfully.
```ts
{
    "predictions": [
        {
            "date": string,
            "value": number
        }
    ]
}
```
