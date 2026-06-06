# fastapi-project1
# Customer Intelligence API (FastAPI)

A production-grade, containerized machine learning inference service built with FastAPI.This API combines a tabular CatBoost model for predicting customer churn risk with an NLTK VADER sentiment analysis engine to process live customer text reviews.

The microservice architecture is highly optimized for performance and memory efficiency by leveraging an in-memory database lookup pattern.


\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
although it has many assumptions such as the columns are in order, feature engineering is hardcoded. this is because i made the churn-prediction model in a kaggle competiiton and when i was implementing a fastapi project i thought i may aswell use that along with fastapi to build a project. thus i have adjusted the project a littile bit to my conviniance. i used the test.csv file from kaggle as the data, converted it into a dic after feature engineering to work as a DB.
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\




## 🏗️ Architectural Design & Optimizations

 This project addresses standard backend performance and MLOps constraints through the following implementations:

### ⚡ Hybrid Startup Memory Caching ($O(1)$ Lookups)
Instead of executing a costly disk-read operation (`pd.read_csv()`) inside the active endpoint for every user request, this service handles data storage processing at boot time. 
The Pandas to Dictionary Pipeline:** Pandas is utilized during server initialization to load the raw historical Kaggle `test.csv` dataset and process heavy feature engineering computations.
Hash-Table Optimization: The data is immediately refactored into a native Python dictionary structure mapping a unique user ID to its matching engineered feature vector list.
This eliminates Pandas overhead during active service and limits database lookup times to a continuous, instantaneous $O(1)$ execution time complexity.
although it has many assumptions suchas the columns are in order. this is because i made the churn-prediction model in a kaggle competiiton and when i was implementing a fastapi project i thought i may aswell use that along with fastapi to build a project. thus i have adjusted the project a littile bit to my conviniance. 

### 🔄 Thread-Pool Concurrency Management
Machine learning model inference involves intense matrix calculations that are inherently CPU-bound[cite: 1591]. 
**Non-Blocking Execution:** Defining the primary routing endpoint using a standard synchronous format (`def predict_customer_intelligence`) instead of an asynchronous declaration (`async def`) signals FastAPI to route computation workloads into a dedicated background worker thread pool. 
This prevents CPU-heavy mathematics from blocking or "hogging" Python’s primary async event loop, ensuring the application remains responsive to incoming requests[cite: 1592, 1657].

### 🛡️ Secure State Isolation (Lifespan Context Manager)
The API entirely avoids dangerous global Python variables to share models and data caches.
It wraps resource initialization inside an explicit `async def lifespan` context manager. 
All assets are safely attached directly to the application state (`request.app.state`) and cleanly emptied from the server's RAM hardware memory (`.clear()`) during a safe container shutdown


### 🔒 Input Hardening & Contract Validation
The service implements strict input and output typing validation via Pydantic schemas. 
The incoming request enforces defensive field constraints (`min_length`, `max_length`, whitespace stripping) to stop malformed payloads or data types from reaching the inference engines, preventing system crashes


---

## 📂 Project Structure

```text
fastapi-project1/
│
├── app.py          # Core FastAPI server application, lifespan context, and endpoints
├── classs.py       # Hardened Pydantic request and response validation schemas
├── requirements.txt# Version-pinned Python dependencies (FastAPI, CatBoost, NLTK, etc.)
├── Dockerfile      # Multi-stage reproducible container environment orchestration
├── churn_model.pkl # Serialized weights of the pre-trained CatBoost tabular classifier
└── test.csv        # Static historical customer feature matrix (Database mock)
