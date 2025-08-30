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
    # Import and include required core routers
    from .routers import analyses, contracts, jobs, reports, rules  # type: ignore
    app.include_router(analyses.router, prefix="/api")
    app.include_router(contracts.router, prefix="/api")
    app.include_router(jobs.router, prefix="/api")
    app.include_router(reports.router, prefix="/api")
    app.include_router(rules.router, prefix="/api")

    # Optional/extended routers (should not break tests if deps missing)
    _include_optional_router(app, "blackletter_api.routers.orchestration")
    _include_optional_router(app, "blackletter_api.routers.gemini")
    _include_optional_router(app, "blackletter_api.routers.risk_analysis")
    _include_optional_router(app, "blackletter_api.routers.admin")

    return app


app = create_app()
