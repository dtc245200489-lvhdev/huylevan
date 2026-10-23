import os
import time
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy import text

db = SQLAlchemy()
REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
LATENCY = Histogram("http_request_duration_seconds", "HTTP request duration", ["endpoint"])
RECIPE_COUNT = Gauge("recipe_records_total", "Number of recipe records")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "local-practice-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://recipe_user:RecipeDB_ChangeMe_2026@localhost:5432/recipes"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    db.init_app(app)

    class Recipe(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(160), nullable=False)
        category = db.Column(db.String(80), nullable=False, default="Món chính")
        ingredients = db.Column(db.Text, nullable=False)
        instructions = db.Column(db.Text, nullable=False)
        prep_minutes = db.Column(db.Integer, nullable=False, default=30)

    app.Recipe = Recipe
    with app.app_context():
        # Retry briefly while PostgreSQL finishes startup; Docker healthcheck is the primary gate.
        for attempt in range(12):
            try:
                db.create_all()
                if db.session.query(Recipe).count() == 0:
                    db.session.add_all([
                        Recipe(title="Phở gà tại nhà", category="Món nước", ingredients="Bánh phở, thịt gà, gừng, hành, rau thơm", instructions="Ninh nước dùng; luộc gà; trụng bánh phở; chan nước dùng và thêm rau.", prep_minutes=60),
                        Recipe(title="Cơm chiên rau củ", category="Món chính", ingredients="Cơm nguội, cà rốt, đậu Hà Lan, trứng, hành lá", instructions="Xào rau củ; thêm trứng và cơm; nêm vừa ăn; đảo đều.", prep_minutes=20),
                        Recipe(title="Salad cà chua dưa leo", category="Món khai vị", ingredients="Cà chua, dưa leo, rau xà lách, dầu ô liu, chanh", instructions="Rửa sạch; cắt lát; trộn sốt dầu ô liu và chanh.", prep_minutes=10),
                    ])
                    db.session.commit()
                break
            except Exception:
                db.session.rollback()
                if attempt == 11:
                    raise
                time.sleep(2)

    @app.before_request
    def start_timer():
        request._started_at = time.perf_counter()

    @app.after_request
    def record_metrics(response):
        endpoint = request.endpoint or "unknown"
        duration = time.perf_counter() - getattr(request, "_started_at", time.perf_counter())
        REQUESTS.labels(request.method, endpoint, str(response.status_code)).inc()
        LATENCY.labels(endpoint).observe(duration)
        return response

    @app.get("/")
    def index():
        q = request.args.get("q", "").strip()
        query = Recipe.query
        if q:
            query = query.filter(Recipe.title.ilike(f"%{q}%") | Recipe.category.ilike(f"%{q}%"))
        recipes = query.order_by(Recipe.id.desc()).all()
        RECIPE_COUNT.set(Recipe.query.count())
        return render_template("index.html", recipes=recipes, q=q)

    @app.get("/recipe/<int:recipe_id>")
    def detail(recipe_id):
        recipe = db.get_or_404(Recipe, recipe_id)
        return render_template("detail.html", recipe=recipe)

    @app.route("/add", methods=["GET", "POST"])
    def add():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            category = request.form.get("category", "Món chính").strip()
            ingredients = request.form.get("ingredients", "").strip()
            instructions = request.form.get("instructions", "").strip()
            try:
                prep = max(1, min(1440, int(request.form.get("prep_minutes", "30"))))
            except ValueError:
                prep = 30
            if not title or not ingredients or not instructions:
                flash("Vui lòng nhập tên món, nguyên liệu và cách làm.", "error")
                return render_template("add.html")
            db.session.add(Recipe(title=title[:160], category=category[:80], ingredients=ingredients, instructions=instructions, prep_minutes=prep))
            db.session.commit()
            app.logger.info("recipe_created title=%s", title[:80])
            flash("Đã thêm công thức mới.", "success")
            return redirect(url_for("index"))
        return render_template("add.html")

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}, 200
        except Exception:
            app.logger.exception("healthcheck_failed")
            return {"status": "error", "database": "unavailable"}, 503

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app
