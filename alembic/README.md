Generic single-database configuration with an async dbapi.
# step to use alembic
- uv run alembic init -t async alembic
- uv run alembic revision --autogenerate
- uv run alembic upgrade head
# change file in env
replace 
```python
target_metadata = None
```
with
```python
target_metadata = SQLModel.metadata
```
#### add this in run_migration online function
```python
if sys.platform == "win32":
        # Psycopg is incompatible with the default ProactorEventLoop on Windows.
        # Use loop_factory to explicitly create a SelectorEventLoop.
        print("Using SelectorEventLoop via loop_factory for Alembic/Psycopg compatibility on Windows...")
        asyncio.run(run_async_migrations(), loop_factory=asyncio.SelectorEventLoop)
```