let config = {}

if (process.env.NODE_ENV === "development") {
    config.BASE_URL = "http://192.168.2.230:8000/api"
} else {
    config.BASE_URL = "/api"
}

config.TASKS_URL = config.BASE_URL + "/tasks"
config.TASKS_STATUS_SUFFIX = "/status"

export default config;
