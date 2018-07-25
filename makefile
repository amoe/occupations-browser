backend_dir = components/backend

pytest = py.test-3


.PHONY: run_frontend run_backend gather_dependencies

run_frontend:
	yarn --cwd components/frontend run dev

run_backend:
	FLASK_APP=components/backend/ov_rest_server.py FLASK_DEBUG=1 flask run

gather_dependencies:
	yarn --cwd components/frontend install

reset_database:
	sh scripts/clear_neo4j.sh
	python3 components/backend/add_sample_data.py

test_backend:
	$(pytest) components/backend/test.py
