import redis

#Establish redis configurations
config = {
	#Use the local host server. It is Redis' default
	"host" : "localhost",

	#Default port used by Redis server
	"port": 6379,

	#Database number
	"db": 0,
}

reed = redis.StrictRedis(**config)