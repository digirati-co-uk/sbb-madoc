# Madoc example config
Example configuration for Madoc. This is a forkable configuration.

## Generating new admin password
Use this tool to generate a new hash:
```
$ bin/generate-password <new secure password>
```

Modify `database/sql/09-user.sql` and swap the password hash there for the one you've generated. 

## Generating new users
To generate a complete new user (sql) you can use this tool. It will output SQL that can be added to the `sql/09-user.sql` file and will be generated on boot.
```
$ bin/generate-user <username> <email> <password> [group]
```
The default group is `global_admin`.

To get started simply run:
```
docker-compose up
```

This will start Madoc on localhost at http://localhost:8898/ with the annotation server available at http://localhost:8899/

## Search
For local development, currently (in pre-release v1.2.x) you have to create the search index manually. Once you have your containers running, you can simply run:
```
curl -X "PUT" "http://localhost:9203/jane-annotations"
```

and this will allow you to start using the statistics module and also start indexing the annotations. Elasticsearch is available at: http://localhost:9203/jane-annotations/_search

and the search interface (Jane Founda) is available at http://localhost:8103/.
