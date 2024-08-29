# Update Backup Status for Service

Allow backup scripts to inform app of backup status.

URL : `/api/status/<service>`

Method : POST

Example :
```
curl -X POST http://localhost:5000/api/status/postgresql
```

## Success Responses

Condition : `service` name is valid and database gets updated successfully.

Code : `200 OK`

Content Example : Response for a successsful `POST` call:
```
{
    'success': True
}
```

## Error Response

Condition : `service` name is invalid.

Code : `400 BAD REQUEST`

Content Example : Response for a bad `POST` call:
```
{
    'success': False, 
    'reason': 'Name must be all letters and/or - symbol only!'
}
```
