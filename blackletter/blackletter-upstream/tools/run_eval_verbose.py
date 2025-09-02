import traceback

from rag.eval import evaluate


if __name__ == "__main__":
    try:
        evaluate.main()
    except Exception:
        traceback.print_exc()
        raise

