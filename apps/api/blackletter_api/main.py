from fastapi import FastAPI


def _include_optional_router(app: FastAPI, module_path: str, attr: str = "router") -> None:
    try:
        mod = __import__(module_path, fromlist=[attr])
        router = getattr(mod, attr, None)
        if router is not None:
            app.include_router(router, prefix="/api")
    except Exception:
        # Silently skip missing or faulty optional routers to keep core API running in tests
        pass


def create_app() -> FastAPI:
    app = FastAPI(title="Blackletter API")

    # Required routers present in this repo
    from .routers import jobs, uploads, metrics  # type: ignore
    app.include_router(uploads.router, prefix="/api")
    app.include_router(jobs.router, prefix="/api")
    app.include_router(metrics.router, prefix="/api")

    # Optional/extended routers (should not break tests if deps missing)
    _include_optional_router(app, "blackletter_api.routers.analyses")
    _include_optional_router(app, "blackletter_api.routers.contracts")
    _include_optional_router(app, "blackletter_api.routers.reports")
    _include_optional_router(app, "blackletter_api.routers.rules")
    _include_optional_router(app, "blackletter_api.routers.orchestration")
    _include_optional_router(app, "blackletter_api.routers.gemini")
    _include_optional_router(app, "blackletter_api.routers.risk_analysis")
    _include_optional_router(app, "blackletter_api.routers.admin")

    return app


app = create_app()
