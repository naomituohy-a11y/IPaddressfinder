from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import io
import pandas as pd
from resolver import resolve_domains

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.lower().endswith((".xlsx",".xls")):
        df = pd.read_excel(io.BytesIO(content))
    else:
        df = pd.read_csv(io.BytesIO(content))

    out = resolve_domains(df)

    buf = io.BytesIO()
    out.to_csv(buf, index=False, encoding="utf-8-sig")
    buf.seek(0)

    output_name = file.filename.rsplit(".", 1)[0] + "_domains.csv"
    return StreamingResponse(buf, media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename=\"{output_name}\"'})
