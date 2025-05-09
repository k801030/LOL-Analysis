# LOL Analysis

> Slowly song please
 
## Preview
![img](preview.png)

## Local Deployment
### Run redis server in background
```
redis-server
```

### Run Flask server
```
flask --app web/server --debug run -p 3000
```

### Run zrok server
```
zrok share public :3000
```