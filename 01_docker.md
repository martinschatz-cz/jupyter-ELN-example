## The Timestamp Method (Easiest)
Use the current date and time as the version. This ensures every build has a unique, chronological ID.

```
APP_VERSION=$(date +%Y%m%d-%H%M%S) docker-compose up --build
```

PowerShell
```
$env:APP_VERSION = Get-Date -Format "yyyyMMdd-HHmm"
docker-compose up --build
```

DOS
```
set APP_VERSION=%date:~10,4%%date:~4,2%%date:~7,2%-%time:~0,2%%time:~3,2%
docker-compose up --build
```