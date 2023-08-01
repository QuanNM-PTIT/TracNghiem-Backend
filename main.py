from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers.user_router import router as UserRouter
from routers.authentication_router import router as AuthenticationRouter
from routers.test_router import router as TestRouter
from routers.topic_router import router as TopicRouter
from routers.question_router import router as QuestionRouter
from routers.storage_router import router as StorageRouter

app = FastAPI()

app.include_router(UserRouter)
app.include_router(AuthenticationRouter)
app.include_router(TestRouter)
app.include_router(TopicRouter)
app.include_router(QuestionRouter)
app.include_router(StorageRouter)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
