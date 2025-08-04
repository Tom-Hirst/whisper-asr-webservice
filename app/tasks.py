from celery import Celery
from app.factory.asr_model_factory import ASRModelFactory
from app.utils import load_audio
import os

celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

asr_model = ASRModelFactory.create_asr_model()
asr_model.load_model()

@celery.task(name="transcribe_task")
def transcribe_task(audio_path, task, language, initial_prompt, vad_filter, word_timestamps, diarize_options, output):
    """
    Celery task for transcribing audio files.
    """
    result = asr_model.transcribe(
        load_audio(audio_path, True),
        task,
        language,
        initial_prompt,
        vad_filter,
        word_timestamps,
        diarize_options,
        output
    )
    os.remove(audio_path)  # Clean up the temporary audio file
    return "".join(list(result))
