import fastapi
import redis
import time
import json

app = fastapi.FastAPI(
    title="API Caching Layer",
    description="Simple FastAPI project using Redis caching",
    version="1.0"
)

# Connect to Redis
cache = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# --------------------------------
# Simulated slow API
# --------------------------------

def get_data_from_source():
    time.sleep(2)

    data = {
        "message": "Data fetched from source",
        "products": [
            "Laptop",
            "Mobile",
            "Keyboard",
            "Mouse"
        ]
    }

    return data


# --------------------------------
# Without Cache
# --------------------------------

@app.get("/without-cache")
def without_cache():

    start_time = time.time()

    data = get_data_from_source()

    end_time = time.time()

    return {
        "source": "API",
        "data": data,
        "time_taken": round(end_time - start_time, 2)
    }


# --------------------------------
# With Redis Cache
# --------------------------------

@app.get("/with-cache")
def with_cache():

    start_time = time.time()

    cached_data = cache.get("products")

    if cached_data:

        data = json.loads(cached_data)

        source = "Redis Cache"

    else:

        data = get_data_from_source()

        cache.set(
            "products",
            json.dumps(data),
            ex=60
        )

        source = "API - New Data"

    end_time = time.time()

    return {
        "source": source,
        "data": data,
        "time_taken": round(end_time - start_time, 4)
    }


# --------------------------------
# Clear Cache
# --------------------------------

@app.delete("/clear-cache")
def clear_cache():

    cache.delete("products")

    return {
        "message": "Cache cleared successfully"
    }


# --------------------------------
# Home
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "API Caching Layer is running",
        "endpoints": [
            "/without-cache",
            "/with-cache",
            "/clear-cache"
        ]
    }