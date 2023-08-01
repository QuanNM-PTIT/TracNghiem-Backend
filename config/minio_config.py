from minio import Minio

minio_client = Minio("localhost:9000", access_key="NE748MyKlEXb0SsMoY7t",
                     secret_key="PvnQLIwSCqo8pMKPUzOEbW6PfgWswwtpaQPwjlVi", secure=False)
