CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    subscription_tier VARCHAR(32) NOT NULL DEFAULT 'free',
    api_key VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transformations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    input_content TEXT NOT NULL,
    input_type VARCHAR(32) NOT NULL,
    parameters JSONB NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'queued',
    source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS outputs (
    id SERIAL PRIMARY KEY,
    transformation_id INTEGER NOT NULL REFERENCES transformations(id) ON DELETE CASCADE,
    format_type VARCHAR(32) NOT NULL,
    content JSONB NOT NULL,
    quality_score DOUBLE PRECISION NOT NULL DEFAULT 80.0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) UNIQUE NOT NULL,
    provider VARCHAR(50) NOT NULL,
    cost_per_1k_tokens DOUBLE PRECISION NOT NULL,
    quality_score DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS api_usage_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    transformation_id INTEGER REFERENCES transformations(id) ON DELETE SET NULL,
    model_name VARCHAR(100) NOT NULL,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    billed_amount DOUBLE PRECISION NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transformations_user_created ON transformations(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_outputs_transform_format ON outputs(transformation_id, format_type);
