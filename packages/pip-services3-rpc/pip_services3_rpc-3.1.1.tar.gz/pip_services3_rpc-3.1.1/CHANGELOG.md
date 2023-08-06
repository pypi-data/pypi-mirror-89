# Communication components for Pip.Services in Python Changelog

## <a name="3.1.1"></a> 3.1.1 (2020-12-21)

### Bug Fixes
* Fixed **HttpResponseSender**, **RestOperations** send_deleted_result methods
* Fix threads in **HttpEndpoint**

## <a name="3.1.0"></a> 3.1.0 (2020-08-04)

### Bug Fixes
* Fixed validation in RestService

## <a name="2.0.0"></a> 2.0.0 (2017-04-05)

### Features
* **rest** Added CommandableHttpService
* **rest** Added CommandableHttpClient
* **direct** Added DirectClient
* **rest** Added processing to_json method in RestClient serialization

### Breaking Changes
* Migrated to **pip-services** 2.0
* Renamed IMessageQueue.getMessageCount to IMessageQueue.readMessageCount

## <a name="1.0.0"></a> 1.0.0 (2017-01-28)

Initial public release

### Features
* **messaging** Abstract and in-memory message queues
* **rest** RESTful service and client
* **seneca** Seneca service and client

### Bug Fixes
No fixes in this version

