from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time


app = FastAPI(
    title="DevOps Group API",
    description="API REST utilisée pour un projet DevOps CI/CD complet.",
    version="1.0.0",
)

tasks = []

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Nombre total de requêtes reçues",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latence des requêtes HTTP",
    ["endpoint"],
)


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class Task(TaskCreate):
    id: int
    done: bool = False


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)

    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "message": "Bienvenue sur l'API DevOps Group",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
    }


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Le titre est obligatoire")

    new_task = Task(
        id=len(tasks) + 1,
        title=task.title,
        description=task.description,
        done=False,
    )

    tasks.append(new_task)
    return new_task


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)